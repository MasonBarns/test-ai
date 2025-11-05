from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from transformers import pipeline
import torch

app = FastAPI()

# Load your model once when the app starts
chatbot = pipeline("text-generation", model="sshleifer/tiny-gpt2")

# Serve the frontend
@app.get("/")
def serve_ui():
    return FileResponse("index.html")

# Handle chat requests
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    if not prompt:
        return JSONResponse(content={"response": "No prompt provided."})

    result = chatbot(prompt, max_length=100, do_sample=True)
    response = result[0]["generated_text"]
    return JSONResponse(content={"response": response})
