from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.core.limiter import limiter

router = APIRouter()

@router.get("/status")
@limiter.limit("5/minute")
async def get_status(request: Request):  # <-- Adiciona `request` aqui
    return JSONResponse(content={"status": "ok"})
