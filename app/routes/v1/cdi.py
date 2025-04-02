# routes/cdi.py

from fastapi import APIRouter, HTTPException, Request
from app.models.cdi import CDI
from datetime import date
import httpx
#from slowapi.decorator import Limiter
from app.middleware.rate_limit import limiter  # ⬅️ importa o limiter

router = APIRouter()

BCB_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/1?formato=json"

@router.get("/cdi", response_model=CDI)
@limiter.limit("10/minute")
async def get_cdi(request: Request):  # ⬅️ Adiciona request aqui
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BCB_URL)
            response.raise_for_status()
            data = response.json()[0]

            return {
                "date": date.fromisoformat(
                    f"{data['data'].split('/')[2]}-{data['data'].split('/')[1]}-{data['data'].split('/')[0]}"
                ),
                "value": float(data["valor"].replace(",", "."))
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar CDI: {str(e)}")
