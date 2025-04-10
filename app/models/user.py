# app/models/user.py

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


# Modelo principal que será mapeado para a tabela no banco
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    score: int = 0
    level: str = "iniciante"
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Modelo para criação de usuários (entrada)
class UserCreate(SQLModel):
    username: str
    email: Optional[str] = None
    password: str


# Modelo para leitura de usuários (retorno da API)
class UserRead(SQLModel):
    id: Optional[int]  # Agora aceita None em casos iniciais
    username: str
    email: Optional[str]
    score: int
    level: str


# Modelo para atualização de usuários (parcial)
class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
    score: Optional[int] = None
    level: Optional[str] = None
