# models/ibov.py

from datetime import date

from pydantic import BaseModel


class Ibov(BaseModel):
    date: date
    close: float  # valor de fechamento do índice
