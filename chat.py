# chat.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import requests
from auth import register_user, get_user_history, save_to_history

router = APIRouter()

# API keys
LANGSEARCH_API_KEY = "sk-dcb31d322a8e4cda94ad1d1630afb5af"
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
    except Exception as e:
        print("LangSearch error:", e)
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
    except Exception as e:
        print("OpenRouter error:", e)
        return "Nova couldn't generate a response."

@router.post("/chat")
async def chat(request: Request):
    data = await request.json()
    email = data.get("email")
    prompt = data.get("prompt")

    if not email or not prompt:
        return JSONResponse(content={"error": "Missing email or prompt"}, status_code=400)

    register_user(email)

    response = search_langsearch(prompt)
    if not response or response.strip() == "":
        response = fallback_openrouter(prompt)

    save_to_history(email, prompt, response)
    history = get_user_history(email)

    return JSONResponse(content={"response": response, "history": history})
