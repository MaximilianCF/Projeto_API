# routes/cambio.py

from fastapi import APIRouter, HTTPException
from app.models.cambio import TaxaCambio
from datetime import date
import httpx

router = APIRouter()

BCB_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/1?formato=json"

@router.get("/usdbrl", response_model=TaxaCambio)
async def get_cambio_usd_brl():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BCB_URL)
            response.raise_for_status()
            data = response.json()[0]

            return {
                "date": date.fromisoformat(data["data"].split("/")[2] + "-" + data["data"].split("/")[1] + "-" + data["data"].split("/")[0]),
                "currency": "USD/BRL",
                "value": float(data["valor"].replace(",", "."))
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar taxa de câmbio: {str(e)}")
