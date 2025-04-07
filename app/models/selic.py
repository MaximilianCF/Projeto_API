from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Selic(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date
    valor: float
