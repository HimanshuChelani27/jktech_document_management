from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    filename = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")
