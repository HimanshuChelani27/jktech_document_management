from fastapi.testclient import TestClient
import io

def test_upload_document(client: TestClient, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    # Create a dummy file in memory
    file_content = b"This is a test document content."
    file = io.BytesIO(file_content)
    file.name = "test_document.txt"

    response = client.post(
        "/api/document/upload_document",
        headers=headers,
        files={"file": (file.name, file, "text/plain")},
        data={"title": "Test Document Title"} # Include title if required by endpoint
    )

    # Check for successful upload (assuming 200 OK)
    # Adjust status code check if your API returns something different (e.g., 201 Created)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "details" in data
    # Access data within the 'details' key
    details = data["details"]
    assert details["title"] == "Test Document Title"
    assert details["filename"] == "test_document.txt"
    assert "document_id" in details

def test_get_all_documents(client: TestClient, auth_token: str):
    # First, upload a document to ensure there's something to retrieve
    test_upload_document(client, auth_token) # Reuse the upload test logic

    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/api/document/documents", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    assert "details" in data
    assert isinstance(data["details"], list)
    # Check if the previously uploaded document is in the list
    details_list = data["details"]
    assert any(doc["filename"] == "test_document.txt" for doc in details_list)

def test_upload_document_unauthenticated(client: TestClient):
    # Create a dummy file
    file_content = b"This is another test document."
    file = io.BytesIO(file_content)
    file.name = "unauth_test.txt"

    response = client.post(
        "/api/document/upload_document",
        files={"file": (file.name, file, "text/plain")},
        data={"title": "Unauthenticated Upload"}
    )
    # Expecting 401 Unauthorized or similar error
    assert response.status_code == 401 # Or 403 Forbidden depending on implementation

def test_get_all_documents_unauthenticated(client: TestClient):
    response = client.get("/api/document/documents")
    # Expecting 401 Unauthorized or similar error
    assert response.status_code == 401 # Or 403 Forbidden