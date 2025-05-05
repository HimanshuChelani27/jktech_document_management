# api/users.py or roles.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import role
from app.core.database import get_db
from app.schemas import role as role_schemas
from app.schemas.response import StandardResponse
from app.utils.response import make_response
router = APIRouter()
@router.get("/roles", response_model=StandardResponse)
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(role.Role).all()
    return make_response([role_schemas.RoleBase.from_orm(r) for r in roles])


