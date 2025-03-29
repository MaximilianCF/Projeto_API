from typing import Optional
from sqlmodel import SQLModel, Field, ForeignKey
from datetime import datetime

class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    challenge_id: int = Field(foreign_key="challenge.id")
    notebook_url: str
    score: float
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
