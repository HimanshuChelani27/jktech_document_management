# seed_data.py

from sqlalchemy.orm import Session
from app.models import role as role_model
from app.models import user as user_model
from app.core.database import SessionLocal, engine
from passlib.context import CryptContext

# Create tables if they don't exist
role_model.Base.metadata.create_all(bind=engine)
user_model.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Seed roles
def seed_roles(db: Session):
    roles = ["admin", "editor", "viewer"]
    for idx, name in enumerate(roles, start=1):
        existing = db.query(role_model.Role).filter_by(name=name).first()
        if not existing:
            role = role_model.Role(role_id=idx, name=name)
            db.add(role)
    db.commit()

# Seed users
def seed_users(db: Session):
    user_data = [
        {
            "email": "admin@example.com",
            "password": "adminpass",
            "full_name": "Admin User",
            "role_id": 1,
        },
        {
            "email": "editor@example.com",
            "password": "editorpass",
            "full_name": "Editor User",
            "role_id": 2,
        },
    ]
    for data in user_data:
        existing = db.query(user_model.User).filter_by(email=data["email"]).first()
        if not existing:
            hashed_password = pwd_context.hash(data["password"])
            user = user_model.User(
                email=data["email"],
                password=hashed_password,
                full_name=data["full_name"],
                role_id=data["role_id"],
            )
            db.add(user)
    db.commit()

def main():
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_users(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
