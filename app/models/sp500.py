# models/sp500.py

from pydantic import BaseModel
from datetime import date

class SP500(BaseModel):
    date: date
    close: float  # pontos do índice
