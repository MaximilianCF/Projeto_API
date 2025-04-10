from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChallengeCreate(BaseModel):
    titulo: str
    descricao: str
    deadline: Optional[datetime] = None


class ChallengeRead(BaseModel):
    id: int
    titulo: str
    descricao: str
    deadline: Optional[datetime] = None
    criado_em: datetime
