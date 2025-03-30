# routes/selic_csv.py

from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import httpx
from io import StringIO

router = APIRouter()

@router.get("/selic-csv")
async def get_selic_csv(
    data_inicial: str = Query(default="01/01/2015"),
    data_final: str = Query(default=None)
):
    try:
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=csv&dataInicial={data_inicial}"
        if data_final:
            url += f"&dataFinal={data_final}"

        headers = {
            "Accept": "text/csv,application/xhtml+xml",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=15.0)

        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text), sep=';', encoding='latin1')
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        df['valor'] = df['valor'].str.replace(',', '.').astype(float)

        return {"selic": df.to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar CSV da SELIC: {str(e)}")
