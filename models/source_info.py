from pydantic import BaseModel

class SourceInfo(BaseModel):
    name: str
    url: str
    access_type: str