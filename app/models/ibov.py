# models/ibov.py

from pydantic import BaseModel
from datetime import date

class Ibovespa(BaseModel):
    date: date
    close: float  # valor de fechamento do índice
