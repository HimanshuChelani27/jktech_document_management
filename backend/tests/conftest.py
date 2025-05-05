import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add project root to the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app  # Import your FastAPI app instance
from app.core.database import Base, get_db

# Use the provided MySQL database for testing
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Himanshu@localhost:3306/document_management"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create the database tables before tests run
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    # Insert a default role
    Session = sessionmaker(bind=engine)
    session = Session()
    from app.models.role import Role
    default_role = Role(role_id=1, name='user')
    session.add(default_role)
    session.commit()
    session.close()
    yield
    # Clean up the database tables after tests
    Base.metadata.drop_all(bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    # Create a TestClient instance
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def auth_token(client: TestClient):
    # Register a user for authentication tests
    client.post(
        "/api/auth/register",
        json={"email": "testauth@example.com", "password": "password123", "role_id": 1} # Ensure role_id 1 exists
    )
    # Login to get the token
    response = client.post(
        "/api/auth/login",
        json={"email": "testauth@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data["details"]
    return data["details"]["access_token"]