from fastapi import APIRouter, Depends
from app.core.security.jwt_auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/api/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Bem-vindo, {current_user.username}!"}
