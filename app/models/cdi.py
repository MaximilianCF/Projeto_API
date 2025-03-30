# models/cdi.py

from pydantic import BaseModel
from datetime import date

class CDI(BaseModel):
    date: date
    value: float  # taxa efetiva diária em %
