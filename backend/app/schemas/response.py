from pydantic import BaseModel
from typing import Any

class StandardResponse(BaseModel):
    code: int
    details: Any


    class Config:
        from_attributes = True