# app/routes/status.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def get_status():
    return {"status": "ok", "message": "API está online 🚀"}
