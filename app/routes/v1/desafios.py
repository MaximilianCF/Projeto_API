from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security.jwt_auth import get_current_user
from app.models.challenge import Challenge
from app.models.user import User
from app.schemas.challenge import ChallengeCreate, ChallengeRead

router = APIRouter()


@router.post("/", response_model=ChallengeRead,
             status_code=status.HTTP_201_CREATED)
async def criar_desafio(
    desafio: ChallengeCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    novo_desafio = Challenge(**desafio.dict())
    session.add(novo_desafio)
    await session.commit()
    await session.refresh(novo_desafio)
    return novo_desafio


@router.get("/", response_model=List[ChallengeRead])
async def listar_desafios(  # <- adicionado async
    session: AsyncSession = Depends(get_session),  # <- alterado para AsyncSession
    current_user: User = Depends(
        get_current_user
    ),  # <- adicionado para bater com o teste
):
    result = await session.execute(select(Challenge))  # <- adicionado await e atribuição a result
    desafios = result.scalars().all()  # <- adicionado atribuição a desafios
    return desafios  # <- alterado para retornar desafios
