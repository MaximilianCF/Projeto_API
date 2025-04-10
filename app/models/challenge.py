from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Challenge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descricao: str
    deadline: Optional[datetime] = None
    criado_em: datetime = Field(default_factory=datetime.utcnow)
