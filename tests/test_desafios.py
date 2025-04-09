from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.core.security.jwt_auth import get_current_user
from app.models.leaderboard import Leaderboard
from app.models.user import User

router = APIRouter()

# Mock de ranking
ranking_falso = [
    {"username": "alice", "pontuacao": 95.2},
    {"username": "bob", "pontuacao": 89.4},
    {"username": "carol", "pontuacao": 77.8},
]


@router.get(
    "/",
    include_in_schema=True,
    response_model=List[Leaderboard],
    summary="Ranking dos usuários",
)
def listar_leaderboard(current_user: User = Depends(get_current_user)):
    return ranking_falso
