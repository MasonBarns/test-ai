from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from transformers import pipeline

app = FastAPI()

# Load lightweight model
chatbot = pipeline("text-generation", model="sshleifer/tiny-gpt2")

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data["prompt"]

    prompt = f"You are Nova, a helpful and friendly AI assistant.\nUser: {user_input}\nAI:"
    response = chatbot(prompt, max_new_tokens=50)[0]["generated_text"].split("AI:")[-1].strip()

    return {"response": response}
