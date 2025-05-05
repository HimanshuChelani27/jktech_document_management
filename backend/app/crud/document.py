from sqlalchemy.orm import Session
from app.models.document import Document

def save_document_to_db(db: Session, title: str, filename: str, user_id: int) -> Document:
    document = Document(
        title=title,
        filename=filename,
        user_id=user_id
    )
    db.add(document)
    db.commit()
    db.refresh(document)
    return document
