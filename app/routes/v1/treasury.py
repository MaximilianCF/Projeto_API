from fastapi import APIRouter, HTTPException, Request
from app.middleware.rate_limit import limiter
from datetime import datetime
from cachetools import TTLCache
import httpx
import os

router = APIRouter()
treasury_cache = TTLCache(maxsize=1, ttl=60)

FRED_API_KEY = os.getenv("FRED_API_KEY=b2e114fe817a6697a6f4f146a3436151")

@router.get("/treasury")
@limiter.limit("10/minute")
async def get_treasury_yield(request: Request):
    if not FRED_API_KEY:
        raise HTTPException(status_code=500, detail="FRED_API_KEY não configurada no .env")

    if "treasury" in treasury_cache:
        return treasury_cache["treasury"]

    url = (
        "https://api.stlouisfed.org/fred/series/observations"
        "?series_id=GS10"
        f"&api_key={FRED_API_KEY}"
        "&file_type=json&sort_order=desc&limit=1"
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

            obs = data["observations"][0]
            result = {
                "data": obs["date"],
                "valor": float(obs["value"])
            }

            treasury_cache["treasury"] = result
            return result

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Erro ao buscar Treasury 10Y: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao processar dados do Treasury 10Y: {str(e)}")
