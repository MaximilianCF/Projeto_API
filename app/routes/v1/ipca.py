# app/routes/ipca.py

from fastapi import APIRouter, HTTPException
import httpx
import logging

router = APIRouter()

@router.get("/ipca", tags=["IPCA"])
async def get_ipca():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            valor = float(data[0]["valor"].replace(",", ".")) if isinstance(data[0]["valor"], str) else float(data[0]["valor"])
            data_ipca = data[0]["data"]
            return {"indicador": "IPCA", "valor": valor, "data": data_ipca}
    except Exception as e:
        logging.error(f"Erro ao buscar IPCA: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar dados do IPCA")
