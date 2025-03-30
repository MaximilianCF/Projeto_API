# models/selic.py

from pydantic import BaseModel
from datetime import date

class SelicMeta(BaseModel):
    date: date
    value: float  # valor da taxa Selic meta em %
