# app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.core.database import get_session
from app.core.security.jwt_auth import pwd_context

router = APIRouter()

# 🔐 Criar novo usuário
@router.post("/users", response_model=UserRead)
def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == user_create.username)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    hashed_pw = pwd_context.hash(user_create.password)
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_pw,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# 📖 Ler usuário por ID
@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# 🛠️ Atualizar usuário
@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if user_update.email is not None:
        user.email = user_update.email
    if user_update.score is not None:
        user.score = user_update.score
    if user_update.level is not None:
        user.level = user_update.level
    if user_update.password is not None:
        user.hashed_password = pwd_context.hash(user_update.password)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# ❌ Deletar usuário
@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    session.delete(user)
    session.commit()
