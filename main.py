from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# LangSearch API
LANGSEARCH_API_KEY = "sk-dcb31d322a8e4cda94ad1d1630afb5af"

# OpenRouter API
OPENROUTER_API_KEY = "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"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"

def search_langsearch(query):
    url = "https://api.langsearch.com/search"
    headers = {
        "Authorization": f"Bearer {LANGSEARCH_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": query,
        "num_results": 1
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        if "results" in data and data["results"]:
            return data["results"][0]["content"]
    except Exception:
        pass
    return None

def fallback_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return "Nova couldn't generate a response."

@app.get("/", response_class=HTMLResponse)
def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt")

    response = search_langsearch(prompt)
    if not response or response.strip() == "":
        response = fallback_openrouter(prompt)

    return JSONResponse(content={"response": response})
