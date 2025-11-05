from fastapi import APIRouter, Request
from transformers import AutoTokenizer, T5ForConditionalGeneration
import torch

router = APIRouter()

# Load model and tokenizer once at startup
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

# Store chat history per user
chat_history = {}

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    email = data.get("email")
    prompt = data.get("prompt")

    if not email or not prompt:
        return {"error": "Missing email or prompt."}

    # Format input and generate response
    inputs = tokenizer(f"Respond helpfully: {prompt}", return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=100)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Save to history
    chat_history.setdefault(email, []).append({
        "prompt": prompt,
        "response": response
    })

    return {
        "response": response,
        "history": chat_history[email]
    }
