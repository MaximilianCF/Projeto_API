from typing import List

from pydantic import BaseModel


class IndicatorMetadata(BaseModel):
    indicator_id: str
    last_updated: str
    periodicity: str
    tags: List[str]
