from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    role = relationship("Role")
