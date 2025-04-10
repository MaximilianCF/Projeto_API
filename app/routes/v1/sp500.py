from datetime import datetime

import httpx
from cachetools import TTLCache
from fastapi import APIRouter, HTTPException, Request

from app.middleware.rate_limit import limiter  # ⬅️ importa o limiter
from app.models.sp500 import SP500

router = APIRouter()

# Cache com no máximo 1 item e TTL de 60 segundos
sp500_cache = TTLCache(maxsize=1, ttl=60)


@router.get("/sp500")
@limiter.limit("10/minute")
async def get_sp500(request: Request):
    if "sp500" in sp500_cache:
        return sp500_cache["sp500"]

    url = "https://query1.finance.yahoo.com/v8/finance/chart/^GSPC?interval=1d&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            value = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
            timestamp = data["chart"]["result"][0]["meta"]["regularMarketTime"]
            dt = datetime.fromtimestamp(timestamp)

            result = {"data": dt.strftime("%Y-%m-%d %H:%M:%S"), "valor": value}

            sp500_cache["sp500"] = result
            return result

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Erro ao buscar S&P500: {str(e)}")
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar S&P500: {str(e)}")