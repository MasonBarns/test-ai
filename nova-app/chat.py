from fastapi import APIRouter, Form, Depends, HTTPException
import httpx, os
from db import save_chat, list_chats
from auth import verify_firebase_id_token

router = APIRouter()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.getenv("OPENROUTER_MODEL", "openchat/openchat-3.5-1210")

async def get_user(auth_token: str = Form(...)):
    user = await verify_firebase_id_token(auth_token)
    return user

@router.post("/chat")
async def chat(
    prompt: str = Form(...),
    user = Depends(get_user)
):
    if not OPENROUTER_API_KEY:
        raise HTTPException(status_code=500, detail="LLM key not configured")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are Nova: concise, accurate, grounded. If unsure, say so."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        if r.status_code >= 400:
            raise HTTPException(status_code=502, detail=f"LLM error: {r.text}")
        data = r.json()
        reply = data["choices"][0]["message"]["content"]

    save_chat(user_id=user["uid"], email=user.get("email", ""), prompt=prompt, response=reply)
    return {"response": reply}

@router.get("/chats")
async def chats(auth_token: str):
    user = await verify_firebase_id_token(auth_token)
    return {"items": list_chats(user_id=user["uid"])}
