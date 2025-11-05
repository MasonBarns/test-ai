from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

LANGSEARCH_API_KEY = "sk-dcb31d322a8e4cda94ad1d1630afb5af"

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
    res = requests.post(url, headers=headers, json=payload)
    data = res.json()
    if "results" in data and data["results"]:
        return data["results"][0]["content"]
    return "No answer found."

@app.get("/", response_class=HTMLResponse)
def serve_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    response = search_langsearch(prompt)
    return JSONResponse(content={"response": response})
