from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Challenge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    dataset_url: str
    deadline: datetime
    prize: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
