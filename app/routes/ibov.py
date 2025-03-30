from fastapi import APIRouter, HTTPException
from app.models.ibov import Ibovespa
from datetime import datetime
import httpx

router = APIRouter()

YF_URL = "https://query1.finance.yahoo.com/v8/finance/chart/^BVSP?interval=1d&range=1d"

@router.get("/ibovespa", response_model=Ibovespa)
async def get_ibovespa():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(YF_URL)
            response.raise_for_status()
            data = response.json()

            result = data["chart"]["result"]
            if not result or "timestamp" not in result[0] or not result[0]["timestamp"]:
                raise ValueError("Dados de IBOV inválidos ou ausentes")

            timestamp = result[0]["timestamp"][0]
            close = result[0]["indicators"]["quote"][0]["close"][0]

            return {
                "date": datetime.fromtimestamp(timestamp).date(),
                "close": close
            }

    except Exception as e:
        print(f"[IBOV ERROR] {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar IBOV: {str(e)}")