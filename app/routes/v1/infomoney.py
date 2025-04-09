import httpx
from fastapi import APIRouter, HTTPException, Request

from app.middleware.rate_limit import limiter
from app.services.webscraping.infomoney_service import fetch_infomoney_headlines

router = APIRouter()


@router.get("/infomoney", tags=["WEBSCRAPING"])
@limiter.limit("10/minute")
async def get_infomoney_news(request: Request):
    try:
        return await fetch_infomoney_headlines()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
