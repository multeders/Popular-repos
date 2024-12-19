from pydantic import BaseModel
from typing import Optional

class Repository(BaseModel):
    id: int
    name: str
    stars: int
    language: Optional[str]
    url: str

