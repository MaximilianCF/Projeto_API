# app/routes/ipca.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/ipca")
def get_ipca():
    return {
        "indicador": "IPCA",
        "valor": 4.12,
        "data": "2025-03-01"
    }
