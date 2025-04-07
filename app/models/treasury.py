# models/treasury.py

from datetime import date

from pydantic import BaseModel


class Treasury(BaseModel):
    date: date
    yield_pct: float  # rendimento anualizado em %
