from fastapi import APIRouter, Query
import httpx

router = APIRouter()

# Simple truth-first search using Wikipedia summaries
@router.get("/search")
async def search(q: str = Query(..., min_length=2)):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q.replace(' ', '_')}"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        if r.status_code == 404:
            return {"source": "wikipedia", "title": q, "summary": "No result found."}
        r.raise_for_status()
        data = r.json()
        return {
            "source": "wikipedia",
            "title": data.get("title"),
            "summary": data.get("extract"),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page")
        }
