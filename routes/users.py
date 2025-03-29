from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from core.database import get_session
from models.user import User
from typing import List

router = APIRouter()

@router.post("/users/", response_model=User, summary="Criar novo usuário")
def create_user(user: User, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/users/", response_model=List[User], summary="Listar usuários")
def read_users(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@router.get("/users/{user_id}", response_model=User, summary="Obter usuário por ID")
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
