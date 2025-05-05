from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi import HTTPException, Depends
# Secret key and algorithm
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
from fastapi.security import OAuth2PasswordBearer

# This should match your token URL endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()  # data should already include 'user_id' and 'role_id'
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = get_jwt_token_data(token)  # This decodes the JWT token and returns user data

        if not payload:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Optional: You can create a function to get the JWT payload with user info
def get_jwt_token_data(token: str):
    try:
        # Decode the token and get the data
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload  # You can return the payload which can include user_id and role
    except JWTError:
        return None
