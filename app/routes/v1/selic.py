# routes/selic.py

import logging
from datetime import date

import httpx
from fastapi import APIRouter, HTTPException, Request

from app.middleware.rate_limit import limiter  # ⬅️ importa o limiter
from app.models.selic import Selic

logging.basicConfig(
    level=logging.INFO,  # Define o nível de log (INFO, DEBUG, ERROR, etc.)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato do log
    handlers=[
        logging.StreamHandler(),  # Envia os logs para o terminal
        logging.FileHandler("app.log"),  # Envia os logs para um arquivo
    ],
)

router = APIRouter()

BCB_URL = (
    "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
)


@router.get("/selic", response_model=Selic)
@limiter.limit("10/minute")
async def get_selic(request: Request):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BCB_URL)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Resposta da API do BCB: {data}")
            
            # Certifique-se de que o JSON retornado tem os campos esperados
            if not data or "data" not in data[0] or "valor" not in data[0]:
                raise HTTPException(status_code=500, detail="Formato inesperado da API do BCB")

            data = data[0]
            return {
                "date": date.fromisoformat(
                    data["data"].split("/")[2]
                    + "-"
                    + data["data"].split("/")[1]
                    + "-"
                    + data["data"].split("/")[0]
                ),
                "value": float(data["valor"].replace(",", ".")),
            }

    except Exception as e:
        logging.error(f"Erro ao buscar SELIC: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar SELIC: {str(e)}"
        )
