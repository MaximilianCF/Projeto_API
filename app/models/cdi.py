# models/cdi.py

from datetime import date

from pydantic import BaseModel


class Cdi(BaseModel):
    date: date
    value: float  # taxa efetiva diária em %
