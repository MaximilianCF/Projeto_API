from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.security.jwt_auth import get_current_user
from app.middleware.rate_limit import limiter  # ⬅️ importa o limiter
from app.models.user import User

router = APIRouter()


@router.get("/protected")
@limiter.limit("10/minute")
def protected_route(
        request: Request,
        current_user: User = Depends(get_current_user)):
    return {"message": f"Bem-vindo, {current_user.username}!"}
