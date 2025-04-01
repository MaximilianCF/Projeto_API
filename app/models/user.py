# app/models/user.py

from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modelo usado no banco de dados
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: Optional[str]
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
