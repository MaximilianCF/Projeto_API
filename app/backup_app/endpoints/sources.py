from fastapi import APIRouter

router = APIRouter()

@router.get("/sources")
def list_sources():
    return []