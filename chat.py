# chat.py
from fastapi import APIRouter, Request
from transformers import pipeline


router = APIRouter()
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

chat_history = {}

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    email = data["email"]
    prompt = data["prompt"]

    inputs = tokenizer(f"Respond helpfully: {prompt}", return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=100)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    chat_history.setdefault(email, []).append({"prompt": prompt, "response": response})
    return {"response": response, "history": chat_history[email]}
