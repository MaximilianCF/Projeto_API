from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    score: int = Field(default=0)
    level: str = Field(default="Bronze")
    created_at: datetime = Field(default_factory=datetime.utcnow)
