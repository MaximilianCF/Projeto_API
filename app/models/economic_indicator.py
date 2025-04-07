from pydantic import BaseModel


class EconomicIndicatorBase(BaseModel):
    id: str
    name: str
    code: str
    frequency: str


class EconomicIndicatorData(BaseModel):
    date: str
    value: float
