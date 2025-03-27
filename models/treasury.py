# models/treasury.py

from pydantic import BaseModel
from datetime import date

class Treasury10Y(BaseModel):
    date: date
    yield_pct: float  # rendimento anualizado em %
