from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ingestion(Base):
    __tablename__ = "ingestions"

    ingestion_id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.document_id"))
    status = Column(String(50))
    started_at = Column(TIMESTAMP, nullable=True)
    finished_at = Column(TIMESTAMP, nullable=True)
    error_message = Column(Text)

    document = relationship("Document")
