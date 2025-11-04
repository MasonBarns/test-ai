from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from transformers import pipeline
import torch  # Required for model loading

app = FastAPI()

# Load a lightweight text generation model
chatbot = pipeline("text-generation", model="sshleifer/tiny-gpt2")

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data["prompt"]

    # Build prompt with personality
    prompt = f"You are Nova, a helpful and friendly AI assistant.\nUser: {user_input}\nAI:"
    response = chatbot(prompt, max_new_tokens=50)[0]["generated_text"].split("AI:")[-1].strip()

    return {"response": response}
