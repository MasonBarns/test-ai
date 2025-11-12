from fastapi import APIRouter, Form, HTTPException
import httpx
import os
from db import save_chat, list_chats

router = APIRouter()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@router.post("/chat")
async def chat(
    prompt: str = Form(...),
    user_id: str = Form(...),
    email: str = Form("")
):
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="OpenRouter API key not configured")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openchat/openchat-3.5-1210",
        "messages": [
            {"role": "system", "content":
             "You are Nova. Be concise, accurate, and warm. If you don’t know, say so. Avoid speculation."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        if r.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"LLM error: {r.text}")
        data = r.json()
        reply = data["choices"][0]["message"]["content"]

    # Save chat
    save_chat(user_id=user_id, email=email, prompt=prompt, response=reply)
    return {"response": reply}

@router.get("/chats")
async def chats(user_id: str):
    return {"items": list_chats(user_id)}
