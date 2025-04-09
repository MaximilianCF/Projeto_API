# app/routes/me.py

from fastapi import APIRouter, Depends

from app.core.security.jwt_auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "score": current_user.score,
        "level": current_user.level,
    }
