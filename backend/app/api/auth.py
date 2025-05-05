from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserCreate, LoginRequest, TokenResponse
from app.core.database import get_db
from app.crud.user import create_user, get_user_by_email
from app.utils.response import make_response
from app.core.security import verify_password, create_access_token
router = APIRouter()
@router.post("/register", response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = create_user(db, user)
    return make_response(
        data=UserOut.from_orm(new_user),
        code=200,
        message="Registration successful"
    )
@router.post("/login", response_model=dict)
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, login.email)
    if not user or not verify_password(login.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": user.email, "role_id": user.role_id, "user_id": user.user_id})

    return make_response(
        data={"access_token": token, "token_type": "bearer"},
        message="Login successful"
    )

