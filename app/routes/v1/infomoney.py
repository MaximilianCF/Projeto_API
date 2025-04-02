from fastapi import APIRouter, HTTPException
from app.services.webscraping.infomoney_service import fetch_infomoney_headlines

router = APIRouter()

@router.get("/infomoney", tags=["WEBSCRAPING"])
def get_infomoney_news():
    try:
        return fetch_infomoney_headlines()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
