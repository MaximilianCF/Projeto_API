from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SubmissionCreate(BaseModel):
    desafio_id: int
    score: Optional[float] = None  # ou resultado enviado


class SubmissionRead(BaseModel):
    id: int
    desafio_id: int
    usuario_id: int
    score: Optional[float]
    enviado_em: datetime
