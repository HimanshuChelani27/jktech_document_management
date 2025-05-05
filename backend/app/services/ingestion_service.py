# import faiss
# import numpy as np
# import pickle
# import os
#
# from fastapi import Depends
#
# from app.utils.azure_utils import generate_azure_embeddings
# from app.utils.file_handler import split_text_into_chunks
# from app.models.document import Document
# from app.core.database import get_db
#
#
# def process_document_ingestion(document_id: int, file_name: str):
#     db_gen = get_db()  # Create generator
#     db = next(db_gen)
#     document = db.query(Document).filter(Document.document_id == document_id).first()
#     if not document:
#         print("Document not found.")
#         return
#
#     # Use absolute path directly for simplicity and reliability
#     file_path = os.path.abspath(f'temp/{file_name}')
#
#     # Check if file exists
#     if not os.path.exists(file_path):
#         print(f"File does not exist at path: {file_path}")
#         return
#
#     # Get file extension to handle different file types
#     _, ext = os.path.splitext(file_name.lower())
#
#     # Handle different file types
#     try:
#         if ext in ['.pdf', '.docx', '.doc', '.xls', '.xlsx', '.ppt', '.pptx']:
#             # For binary files, try to read from document.content if available
#             if hasattr(document, 'content') and document.content:
#                 content = document.content
#             else:
#                 # Read binary file as binary and decode with error handling
#                 with open(file_path, 'rb') as f:
#                     content = f.read().decode('utf-8', errors='ignore')
#                 print(f"Read binary file with error handling: {file_name}")
#         else:
#             # For text files, try UTF-8 first with error handling as fallback
#             try:
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     content = f.read()
#             except UnicodeDecodeError:
#                 with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
#                     content = f.read()
#                 print(f"Used UTF-8 with error ignoring for {file_name}")
#     except Exception as e:
#         print(f"Error reading file {file_path}: {str(e)}")
#         return
#
#     # Process the content
#     chunks = split_text_into_chunks(content)
#     embeddings = generate_azure_embeddings(chunks)
#
#     # Convert to numpy array for FAISS
#     vectors = np.array(embeddings).astype('float32')
#
#     # Create a FAISS index
#     dim = vectors.shape[1]
#     index = faiss.IndexFlatL2(dim)
#     index.add(vectors)
#
#     # Save metadata (chunk text)
#     metadata = {i: chunks[i] for i in range(len(chunks))}
#
#     # Save FAISS index and metadata to disk
#     index_dir = f"faiss_indexes/{document_id}"
#     os.makedirs(index_dir, exist_ok=True)
#
#     faiss.write_index(index, f"{index_dir}/index.faiss")
#
#     with open(f"{index_dir}/metadata.pkl", "wb") as f:
#         pickle.dump(metadata, f)
#
#     print(f"Saved FAISS index and metadata for document_id: {document_id}")

import faiss
import numpy as np
import pickle
import os
import datetime

from fastapi import Depends

from app.utils.azure_utils import generate_azure_embeddings
from app.utils.file_handler import split_text_into_chunks
from app.models.document import Document
from app.models.ingestion import Ingestion
from app.core.database import get_db


def process_document_ingestion(document_id: int, file_name: str):
    db_gen = get_db()  # Create generator
    db = next(db_gen)
    document = db.query(Document).filter(Document.document_id == document_id).first()
    if not document:
        print("Document not found.")
        return

    # Create or update ingestion record
    ingestion = db.query(Ingestion).filter(Ingestion.document_id == document_id).first()
    if not ingestion:
        ingestion = Ingestion(
            document_id=document_id,
            status="PROCESSING",
            started_at=datetime.datetime.now()
        )
        db.add(ingestion)
    else:
        ingestion.status = "PROCESSING"
        ingestion.started_at = datetime.datetime.now()
        ingestion.error_message = None  # Clear any previous errors

    db.commit()

    # Use absolute path directly for simplicity and reliability
    file_path = os.path.abspath(f'temp/{file_name}')

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"File does not exist at path: {file_path}")
        return

    # Get file extension to handle different file types
    _, ext = os.path.splitext(file_name.lower())

    # Handle different file types
    try:
        if ext in ['.pdf', '.docx', '.doc', '.xls', '.xlsx', '.ppt', '.pptx']:
            # For binary files, try to read from document.content if available
            if hasattr(document, 'content') and document.content:
                content = document.content
            else:
                # Read binary file as binary and decode with error handling
                with open(file_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')
                print(f"Read binary file with error handling: {file_name}")
        else:
            # For text files, try UTF-8 first with error handling as fallback
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                print(f"Used UTF-8 with error ignoring for {file_name}")
    except Exception as e:
        error_msg = f"Error reading file {file_path}: {str(e)}"
        print(error_msg)

        # Update ingestion record with error
        ingestion = db.query(Ingestion).filter(Ingestion.document_id == document_id).first()
        if ingestion:
            ingestion.status = "FAILED"
            ingestion.error_message = error_msg
            ingestion.finished_at = datetime.datetime.now()
            db.commit()
            print(f"Updated ingestion status to FAILED for document_id: {document_id}")
        return

    # Process the content
    chunks = split_text_into_chunks(content)
    embeddings = generate_azure_embeddings(chunks)

    # Convert to numpy array for FAISS
    vectors = np.array(embeddings).astype('float32')

    # Create a FAISS index
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    # Save metadata (chunk text)
    metadata = {i: chunks[i] for i in range(len(chunks))}

    # Save FAISS index and metadata to disk
    index_dir = f"faiss_indexes/{document_id}"
    os.makedirs(index_dir, exist_ok=True)

    faiss.write_index(index, f"{index_dir}/index.faiss")

    try:
        with open(f"{index_dir}/metadata.pkl", "wb") as f:
            pickle.dump(metadata, f)

        print(f"Saved FAISS index and metadata for document_id: {document_id}")
    except Exception as e:
        error_msg = f"Error saving metadata for document_id {document_id}: {str(e)}"
        print(error_msg)

        # Update ingestion record with error
        ingestion = db.query(Ingestion).filter(Ingestion.document_id == document_id).first()
        if ingestion:
            ingestion.status = "FAILED"
            ingestion.error_message = error_msg
            ingestion.finished_at = datetime.datetime.now()
            db.commit()
            print(f"Updated ingestion status to FAILED for document_id: {document_id}")
        return

    # Update ingestion record to COMPLETED
    ingestion = db.query(Ingestion).filter(Ingestion.document_id == document_id).first()
    if ingestion:
        ingestion.status = "COMPLETED"
        ingestion.finished_at = datetime.datetime.now()
        db.commit()
        print(f"Updated ingestion status to COMPLETED for document_id: {document_id}")