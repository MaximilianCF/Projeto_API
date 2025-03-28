# routes/selic_csv.py

from fastapi import APIRouter, HTTPException
import pandas as pd
import requests
from io import StringIO

router = APIRouter()

CSV_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=csv"

@router.get("/selic-csv")
async def get_selic_csv():
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()

        # Lê o CSV diretamente da resposta
        df = pd.read_csv(StringIO(response.text), sep=';', encoding='latin1')

        # Converte para dict com formatação limpa
        df['data'] = pd.to_datetime(df['data'], dayfirst=True)
        df['valor'] = df['valor'].str.replace(',', '.').astype(float)

        # Organiza como lista de dicionários
        data = df.to_dict(orient="records")
        return {"selic": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar CSV da SELIC: {str(e)}")
