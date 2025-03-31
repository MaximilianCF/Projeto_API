# routes/selic_csv.py
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
import pandas as pd
import httpx
from io import StringIO
import logging
import asyncio

router = APIRouter()

# Configuração de logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@router.get("/selic-csv")
async def get_selic_csv(
    data_inicial: str = Query(default="01/01/2015"),
    data_final: str = Query(default=None)
):
    try:
        if not data_final:
            data_final = datetime.now().strftime("%d/%m/%Y")

        params = {
            "formato": "csv",
            "dataInicial": data_inicial,
            "dataFinal": data_final
        }

        headers = {
            "Accept": "text/csv",
            "User-Agent": "python-httpx/0.27.0"
        }

        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados"

        # Retry simples: tenta até 3 vezes
        for tentativa in range(3):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url, params=params, headers=headers, timeout=30.0)

                logger.debug(f"Tentativa {tentativa + 1} | Status: {response.status_code}")
                logger.debug(f"URL requisitada: {response.url}")
                logger.debug(f"Resposta (primeiros 500 caracteres): {response.text[:500]}")

                # Se resposta for 504 (Gateway Timeout do BCB)
                if response.status_code == 504:
                    raise HTTPException(
                        status_code=504,
                        detail="O Banco Central está temporariamente indisponível. Tente novamente em alguns minutos."
                    )

                if response.status_code == 200:
                    break  # Sucesso, sai do loop
            except httpx.RequestError as e:
                logger.warning(f"Erro na tentativa {tentativa + 1}: {e}")
                if tentativa < 2:
                    await asyncio.sleep(2)
                else:
                    raise

        # Se status final não for sucesso, lança erro genérico
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Erro na requisição para o BCB: {response.text}"
            )

        df = pd.read_csv(StringIO(response.text), sep=';', encoding='latin1')
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        df['valor'] = df['valor'].str.replace(',', '.').astype(float)

        return {"selic": df.to_dict(orient="records")}

    except Exception as e:
        detail = f"{e.__class__.__name__}: {str(e)}"
        raise HTTPException(status_code=500, detail=f"Erro ao processar CSV da SELIC: {detail}")
