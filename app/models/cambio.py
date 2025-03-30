# models/cambio.py

from pydantic import BaseModel
from datetime import date
from typing import Literal

class TaxaCambio(BaseModel):
    date: date
    currency: Literal["USD/BRL"]
    value: float  # valor de fechamento
