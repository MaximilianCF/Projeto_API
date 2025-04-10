from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.security.jwt_auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", summary="Submeter solução para um desafio")
async def submit_solution(
    challenge_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400,
                            detail="Apenas arquivos CSV são aceitos.")

    # Simulação: apenas confirma o recebimento
    return {
        "message": "Submissão recebida com sucesso.",
        "usuario": current_user.username,
        "arquivo": file.filename,
        "desafio_id": challenge_id,
    }


@router.get("/", summary="Listar submissões do usuário")
async def list_user_submissions(
        current_user: User = Depends(get_current_user)):
    # Simulação: retorna submissões mockadas
    return [
        {"desafio_id": 1, "arquivo": "solucao1.csv", "status": "pendente"},
        {"desafio_id": 2, "arquivo": "modelo.csv", "status": "avaliado"},
    ]
