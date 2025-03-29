from fastapi import APIRouter
from datetime import date

router = APIRouter()

@router.get("/", summary="Cotação mockada do Dólar Comercial (USD/BRL)")
def get_usdbrl():
    return {
        "data": str(date.today()),
        "compra": 4.89,
        "venda": 4.91,
        "fonte": "Banco Central do Brasil (Mock)"
    }
