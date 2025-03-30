from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class ChallengeBase(SQLModel):
    title: str
    description: str
    dataset_url: str
    deadline: datetime
    prize: Optional[float] = None

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeRead(ChallengeBase):
    id: int
    created_at: datetime

class Challenge(ChallengeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
