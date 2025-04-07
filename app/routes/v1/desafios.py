from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.security.jwt_auth import get_current_user
from app.models.challenge import Challenge
from app.models.user import User
from app.schemas.challenge import ChallengeCreate, ChallengeRead

router = APIRouter()


@router.post("/", response_model=ChallengeRead,
             status_code=status.HTTP_201_CREATED)
def criar_desafio(
    desafio: ChallengeCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    novo_desafio = Challenge(**desafio.dict())
    session.add(novo_desafio)
    session.commit()
    session.refresh(novo_desafio)
    return novo_desafio


@router.get("/", response_model=List[ChallengeRead])
def listar_desafios(
    session: Session = Depends(get_session),
    current_user: User = Depends(
        get_current_user
    ),  # <- adicionado para bater com o teste
):
    desafios = session.exec(select(Challenge)).all()
    return desafios
