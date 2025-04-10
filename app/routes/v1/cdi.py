# routes/cdi.py

from datetime import date

import httpx
from fastapi import APIRouter, HTTPException, Request

# from slowapi.decorator import Limiter
from app.middleware.rate_limit import limiter  # ⬅️ importa o limiter
from app.models.cdi import Cdi

router = APIRouter()

BCB_URL = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/1?formato=json"
)


@router.get("/cdi", response_model=Cdi)
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
                "value": float(data["valor"].replace(",", ".")),
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar CDI: {str(e)}")
