from pydantic import BaseModel

class RoleBase(BaseModel):
    role_id: int
    name: str

    class Config:
        from_attributes = True
