from pydantic import BaseModel
from typing import List

class IndicatorMetadata(BaseModel):
    indicator_id: str
    last_updated: str
    periodicity: str
    tags: List[str]