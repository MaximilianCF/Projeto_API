# app/models/user.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


# Modelo usado no banco de dados
class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    score: int = 0
    level: str = "iniciante"
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Modelos auxiliares para criação, leitura e atualização


class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: Optional[str]
    score: int
    level: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    score: Optional[int] = None
    level: Optional[str] = None
