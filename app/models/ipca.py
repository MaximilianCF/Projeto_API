# models/cdi.py

from datetime import date

from pydantic import BaseModel


class Ipca(BaseModel):
    date: date
    value: float  # taxa efetiva diária em %
