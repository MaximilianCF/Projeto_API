from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    username: str
    email: str
    hashed_password: str
    score: int = 0
    level: str = "Bronze"

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    created_at: datetime

class User(UserBase, table=True):
    __table_args__ = {"extend_existing": True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserUpdate(SQLModel):
    email: str
    level: str = "Bronze"
