from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.core.blobs_storage import upload_file_to_blob
from app.models.document import Document
from app.schemas.document import DocumentOut, StandardResponse, StandardResponseList
from app.crud.document import save_document_to_db
from app.core.security import get_current_user
from app.core.database import get_db
import os
from app.services.ingestion_service import process_document_ingestion
from fastapi import BackgroundTasks
router = APIRouter()
@router.post("/upload_document", response_model=StandardResponse)
def upload_document(
        file: UploadFile = File(...),
        title: str = "",
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user),  # Assuming JWT-based user authentication
        background_tasks: BackgroundTasks = BackgroundTasks()  # For background processing
):
    # Check if the user is authorized (admin or viewer)
    print(current_user)
    if 'role_id' not in current_user:
        raise HTTPException(status_code=400, detail="role_id not found in token payload")

    # Save the file locally (temporary) or directly upload it to Azure Blob
    print(file.filename, "filename")
    file_location = f"temp/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    try:
        # Upload the file to Azure Blob Storage
        file_url = upload_file_to_blob(file_location, file.filename)

        # Save the document details (file URL, title, etc.) in the database
        document = save_document_to_db(db, title, file_url, current_user['user_id'])
        background_tasks.add_task(process_document_ingestion, document.document_id, file.filename)

        # Return the response using StandardResponse
        return StandardResponse(
            code=200,
            details=DocumentOut(  # Ensure you provide the correct document fields here
                document_id=document.document_id,
                title=document.title,
                filename=document.filename,
                user_id=document.user_id,
                created_at=document.created_at
            )
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.get("/documents", response_model=StandardResponseList)  # Use StandardResponseList here
def get_all_documents(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    try:
        # Query the database to get all documents
        documents = db.query(Document).all()

        if not documents:
            raise HTTPException(status_code=404, detail="No documents found")


        # Map the documents to DocumentOut and return as a list in StandardResponseList
        return StandardResponseList(
            code=200,
            details=[DocumentOut(  # Map each document to DocumentOut schema
                document_id=document.document_id,
                title=document.title,
                filename=document.filename,
                user_id=document.user_id,
                created_at=document.created_at
            ) for document in documents]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching documents: {str(e)}")