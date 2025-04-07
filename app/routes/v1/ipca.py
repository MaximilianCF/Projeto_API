# app/routes/ipca.py

from fastapi import APIRouter, HTTPException, Request

from app.middleware.rate_limit import limiter  # ⬅️ importa o limiter

router = APIRouter()


@router.get("/ipca")
@limiter.limit("10/minute")
def get_ipca(request: Request):
    return {"indicador": "IPCA", "valor": 4.12, "data": "2025-03-01"}
