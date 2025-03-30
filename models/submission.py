from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, ForeignKey

class SubmissionBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    challenge_id: int = Field(foreign_key="challenge.id")
    notebook_url: str
    score: float

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionRead(SubmissionBase):
    id: int
    submitted_at: datetime

class Submission(SubmissionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
