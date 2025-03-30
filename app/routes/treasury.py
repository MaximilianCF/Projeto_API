# routes/treasury.py

from fastapi import APIRouter, HTTPException
from app.models.treasury import Treasury10Y
from datetime import datetime
import httpx
import os

router = APIRouter()

FRED_API_KEY = os.getenv("FRED_API_KEY")
FRED_URL = f"https://api.stlouisfed.org/fred/series/observations?series_id=GS10&api_key={FRED_API_KEY}&file_type=json&sort_order=desc&limit=1"

@router.get("/treasury-10y", response_model=Treasury10Y)
async def get_treasury_yield():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(FRED_URL)
            response.raise_for_status()
            data = response.json()

            obs = data["observations"][0]
            return {
                "date": datetime.strptime(obs["date"], "%Y-%m-%d").date(),
                "yield_pct": float(obs["value"])
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar Treasury 10Y: {str(e)}")
