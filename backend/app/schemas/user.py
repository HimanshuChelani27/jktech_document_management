from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role_id: Optional[int] = None

class UserOut(BaseModel):
    user_id: int
    email: EmailStr
    full_name: Optional[str]

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
