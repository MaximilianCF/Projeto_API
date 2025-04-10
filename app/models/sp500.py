# models/sp500.py

from datetime import date

from pydantic import BaseModel


class SP500(BaseModel):
    date: date
    close: float  # pontos do índice
