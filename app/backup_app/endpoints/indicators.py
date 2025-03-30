from fastapi import APIRouter

router = APIRouter()

@router.get("/indicators")
def list_indicators():
    return []

@router.get("/indicators/{id}")
def get_indicator(id: str):
    return {"id": id}