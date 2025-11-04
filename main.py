from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from transformers import AutoTokenizer, AutoModelForCausalLM

app = FastAPI()

# Load a tiny model that fits Koyeb's free tier
tokenizer = AutoTokenizer.from_pretrained("sshleifer/tiny-gpt2")
model = AutoModelForCausalLM.from_pretrained("sshleifer/tiny-gpt2")

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data["prompt"]

    # Format prompt with assistant personality
    prompt = f"You are Nova, a helpful and friendly AI assistant.\nUser: {user_input}\nAI:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).split("AI:")[-1].strip()

    return {"response": response}
