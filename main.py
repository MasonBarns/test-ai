from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from transformers import pipeline
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

chatbot = pipeline("text-generation", model="sshleifer/tiny-gpt2")

def search_duckduckgo(query):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1
    }
    res = requests.get(url, params=params)
    data = res.json()
    return data.get("Abstract") or "No answer found."

@app.get("/", response_class=HTMLResponse)
def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt")

    if "search" in prompt.lower() or "how old is" in prompt.lower():
        response = search_duckduckgo(prompt)
    else:
        result = chatbot(prompt, max_length=100, do_sample=True)
        response = result[0]["generated_text"]

    return JSONResponse(content={"response": response})
