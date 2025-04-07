from datetime import datetime

import httpx
from cachetools import TTLCache
from fastapi import APIRouter, HTTPException, Request

from app.middleware.rate_limit import limiter

router = APIRouter()

# Cache com no máximo 1 item e 60 segundos de TTL
ibov_cache = TTLCache(maxsize=1, ttl=60)


@router.get("/ibov")
@limiter.limit("10/minute")
async def get_ibov(request: Request):
    if "ibov" in ibov_cache:
        return ibov_cache["ibov"]

    url = "https://query1.finance.yahoo.com/v8/finance/chart/^BVSP?interval=1d&range=1d"
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

            ibov_cache["ibov"] = result
            return result

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Erro ao buscar IBOV: {str(e)}")
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar IBOV: {str(e)}")
                        