# routes/selic.py

from fastapi import APIRouter, HTTPException
from app.models.selic import SelicMeta
from datetime import date
import httpx

router = APIRouter()

BCB_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"

@router.get("/selic-meta", response_model=SelicMeta)
async def get_selic_meta():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BCB_URL)
            response.raise_for_status()
            data = response.json()[0]

            return {
                "date": date.fromisoformat(data["data"].split("/")[2] + "-" + data["data"].split("/")[1] + "-" + data["data"].split("/")[0]),
                "value": float(data["valor"].replace(",", "."))
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar SELIC: {str(e)}")
