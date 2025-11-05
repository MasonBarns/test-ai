from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from transformers import AutoTokenizer, T5ForConditionalGeneration

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

chat_history = {}

@app.get("/")
def serve_frontend():
    return FileResponse("index.html")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data["prompt"]
    user_email = data["email"]

    prompt = f"Respond helpfully and kindly: {user_input}"
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_new_tokens=100)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    if user_email not in chat_history:
        chat_history[user_email] = []
    chat_history[user_email].append({"prompt": user_input, "response": response})

    return {"response": response, "history": chat_history[user_email]}
