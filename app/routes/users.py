from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.user import User, UserCreate, UserRead
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/users/register", response_model=UserRead)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    # Verifica se já existe usuário com o mesmo username ou email
    existing_user = session.exec(
        select(User).where((User.username == user_create.username) | (User.email == user_create.email))
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário ou e-mail já registrado.")

    # Cria o hash da senha
    hashed_password = pwd_context.hash(user_create.hashed_password)

    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

from fastapi import APIRouter, Depends
from app.core.security.jwt_auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/users/me", response_model=dict)
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "score": current_user.score,
        "level": current_user.level,
        "created_at": current_user.created_at,
    }
