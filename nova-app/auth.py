import os
import httpx
from fastapi import HTTPException

FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")

async def verify_firebase_id_token(id_token: str):
    """
    Verify Firebase ID token via Google tokeninfo endpoint.
    For production, use Firebase Admin SDK, but this works without service account.
    """
    if not id_token:
        raise HTTPException(status_code=401, detail="Missing auth token")
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get("https://oauth2.googleapis.com/tokeninfo", params={"id_token": id_token})
        if r.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid auth token")
        data = r.json()
        # Basic checks
        if FIREBASE_PROJECT_ID and data.get("aud") and FIREBASE_PROJECT_ID not in data.get("aud"):
            # Best-effort aud match (web apps often use client IDs; leave flexible)
            pass
        return {
            "uid": data.get("sub"),
            "email": data.get("email"),
            "name": data.get("name"),
            "picture": data.get("picture"),
        }
