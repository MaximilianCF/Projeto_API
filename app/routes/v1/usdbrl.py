from fastapi import APIRouter, HTTPException, Request
from app.middleware.rate_limit import limiter  # ⬅️ importa o limiter
from datetime import date

router = APIRouter()

@router.get("/usdbrl", summary="Cotação mockada do Dólar Comercial (USD/BRL)")
@limiter.limit("10/minute")
def get_usdbrl(request: Request):
    return {
        "data": str(date.today()),
        "compra": 4.89,
        "venda": 4.91,
        "fonte": "Banco Central do Brasil (Mock)"
    }
