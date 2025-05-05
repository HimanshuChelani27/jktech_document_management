from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
class DocumentCreate(BaseModel):
    title: str
    filename: str
    file_url: Optional[str] = None  # This could be the link to the uploaded file

    class Config:
        from_attributes = True
class DocumentOut(BaseModel):
    document_id: int
    title: str
    filename: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class StandardResponse(BaseModel):
    code: int
    details: DocumentOut  # Specify DocumentOut as the type for details

    class Config:
        from_attributes = True

class StandardResponseList(BaseModel):
    code: int
    details: List[DocumentOut]  # Expect a list of DocumentOut instead of a single instance

    class Config:
        from_attributes = True