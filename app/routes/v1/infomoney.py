from fastapi import APIRouter, HTTPException, Request
from app.middleware.rate_limit import limiter  # ⬅️ importa o limiter
from app.services.webscraping.infomoney_service import fetch_infomoney_headlines

router = APIRouter()

@router.get("/infomoney", tags=["WEBSCRAPING"])
@limiter.limit("10/minute")
def get_infomoney_news(request: Request):
    try:
        return fetch_infomoney_headlines()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
