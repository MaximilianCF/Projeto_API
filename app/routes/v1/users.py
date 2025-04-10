# app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.database import get_session
from app.core.security.jwt_auth import pwd_context
from app.models.user import User, UserCreate, UserRead, UserUpdate

router = APIRouter()

# 🔐 Criar novo usuário
@router.post("/users", response_model=UserRead)
async def create_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    existing = await session.execute(
        select(User).where(User.username == user_create.username)
    )
    existing_user = existing.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    hashed_pw = pwd_context.hash(user_create.password)
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_pw,
    )
    session.add(new_user)
    await session.commit()             # 👈 importante: await aqui
    await session.refresh(new_user)   # 👈 também await aqui
    return new_user

# 📖 Ler usuário por ID
@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

# 🛠️ Atualizar usuário
@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_session)
):
    user = await session.get(User, user_id)
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
    await session.commit()            # 👈 await aqui também
    await session.refresh(user)      # 👈 e aqui
    return user

# ❌ Deletar usuário
@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    await session.delete(user)
    await session.commit()           # 👈 aqui já estava ok
