from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
def get_status():
    return {"status": "API rodando com sucesso!", "versao": "0.1"}
