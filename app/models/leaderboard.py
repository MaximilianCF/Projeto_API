from typing import Optional

from sqlmodel import Field, SQLModel


class Leaderboard(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    pontuacao: float
