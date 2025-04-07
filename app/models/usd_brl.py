# models/cambio.py

from datetime import date
from typing import Literal

from pydantic import BaseModel


class Usd_brl(BaseModel):
    date: date
    currency: Literal["USD/BRL"]
    value: float  # valor de fechamento
