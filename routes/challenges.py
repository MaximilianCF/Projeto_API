from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from core.database import get_session
from models.challenge import Challenge, ChallengeCreate, ChallengeRead

router = APIRouter()

@router.post("/", response_model=ChallengeRead, summary="Criar novo desafio")
def create_challenge(challenge: ChallengeCreate, session: Session = Depends(get_session)):
    new_challenge = Challenge.from_orm(challenge)
    session.add(new_challenge)
    session.commit()
    session.refresh(new_challenge)
    return new_challenge

@router.get("/", response_model=List[ChallengeRead], summary="Listar desafios")
def read_challenges(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    challenges = session.exec(select(Challenge).offset(offset).limit(limit)).all()
    return challenges

@router.get("/{challenge_id}", response_model=ChallengeRead, summary="Detalhes do desafio")
def read_challenge(challenge_id: int, session: Session = Depends(get_session)):
    challenge = session.get(Challenge, challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    return challenge
