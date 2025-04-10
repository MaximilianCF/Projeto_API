from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    desafio_id: int
    usuario_id: int
    score: Optional[float] = None
    enviado_em: datetime = Field(default_factory=datetime.utcnow)
