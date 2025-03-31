# app/routes/infomoney.py

from fastapi import APIRouter, HTTPException
import httpx
from bs4 import BeautifulSoup

router = APIRouter()

@router.get("/webscraping/infomoney")
async def get_infomoney_headlines():
    url = "https://www.infomoney.com.br/mercados/"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=15.0)
            response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")

        # Seleciona títulos com base no seletor usado no site
        headlines = [
            h2.get_text(strip=True)
            for h2 in soup.select("h2.title")
        ]

        if not headlines:
            raise HTTPException(status_code=404, detail="Nenhuma manchete encontrada.")

        return {"manchetes": headlines[:10]}  # Retorna só as 10 primeiras para evitar poluir
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar manchetes: {str(e)}")
