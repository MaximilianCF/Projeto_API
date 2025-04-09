# app/routes/v1/usd_brl.py

from fastapi import APIRouter, HTTPException, Request
import httpx
from datetime import datetime
from cachetools import TTLCache

from app.middleware.rate_limit import limiter

router = APIRouter()

usdbrl_cache = TTLCache(maxsize=1, ttl=60)


@router.get("/usd_brl", summary="Cotação atual do Dólar Comercial (USD/BRL)")
@limiter.limit("10/minute")
async def get_usdbrl(request: Request):
    if "usdbrl" in usdbrl_cache:
        return usdbrl_cache["usdbrl"]

    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            raw_data = response.json()

        usd_data = raw_data["USDBRL"]
        result = {
            "moeda": "USD/BRL",
            "data": usd_data["create_date"],
            "compra": float(usd_data["bid"]),
            "venda": float(usd_data["ask"]),
            "fonte": "AwesomeAPI"
        }

        usdbrl_cache["usdbrl"] = result
        return result

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Erro ao buscar cotação: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")
