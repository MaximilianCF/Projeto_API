from fastapi import APIRouter

router = APIRouter()

@router.get("/metadata")
def get_all_metadata():
    return []