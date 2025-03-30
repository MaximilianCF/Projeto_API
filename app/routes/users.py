from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.user import User, UserCreate, UserRead
from typing import List

router = APIRouter()

@router.post("/users/", response_model=UserRead, summary="Criar novo usuário")
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    new_user = User.from_orm(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/users/", response_model=List[UserRead], summary="Listar usuários")
def read_users(offset: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users

@router.get("/users/{user_id}", response_model=UserRead, summary="Obter usuário por ID")
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
