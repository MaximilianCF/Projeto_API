import os
from datetime import datetime
from dotenv import load_dotenv
import httpx
from cachetools import TTLCache
from fastapi import APIRouter, HTTPException, Request

from app.middleware.rate_limit import limiter

load_dotenv()

router = APIRouter()
treasury_cache = TTLCache(maxsize=1, ttl=60)

FRED_API_KEY = os.getenv("FRED_API_KEY")
if not FRED_API_KEY:
    raise ValueError("FRED_API_KEY não configurada no .env")

@router.get("/treasury")
@limiter.limit("10/minute")
async def get_treasury(request: Request):
    if not FRED_API_KEY:
        raise ValueError("FRED_API_KEY não configurada no .env")

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
            result = {"data": obs["date"], "valor": float(obs["value"])}

            treasury_cache["treasury"] = result
            return result

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Erro ao buscar Treasury: {str(e)}")
        
    except Exception as e:
        logging.error(f"Erro na rota /treasury: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")
            
