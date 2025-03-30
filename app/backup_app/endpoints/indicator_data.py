from fastapi import APIRouter

router = APIRouter()

@router.get("/indicators/{id}/data")
def get_indicator_data(id: str):
    return []