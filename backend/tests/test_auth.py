from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    response = client.post(
        "/api/auth/register",
        json={"email": "testuser@example.com", "password": "password123", "role_id": 1} # Assuming role_id 1 exists or is created
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Registration successful"
    assert "user_id" in data["details"]
    assert data["details"]["email"] == "testuser@example.com"

def test_register_existing_user(client: TestClient):
    # First registration
    client.post(
        "/api/auth/register",
        json={"email": "existing@example.com", "password": "password123", "role_id": 1}
    )
    # Attempt to register again with the same email
    response = client.post(
        "/api/auth/register",
        json={"email": "existing@example.com", "password": "anotherpassword", "role_id": 1}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_user(client: TestClient):
    # Register user first
    client.post(
        "/api/auth/register",
        json={"email": "loginuser@example.com", "password": "password123", "role_id": 1}
    )
    # Attempt login
    response = client.post(
        "/api/auth/login",
        json={"email": "loginuser@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert "access_token" in data["details"]
    assert data["details"]["token_type"] == "bearer"

def test_login_invalid_password(client: TestClient):
    # Register user first
    client.post(
        "/api/auth/register",
        json={"email": "invalidpass@example.com", "password": "password123", "role_id": 1}
    )
    # Attempt login with wrong password
    response = client.post(
        "/api/auth/login",
        json={"email": "invalidpass@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"

def test_login_nonexistent_user(client: TestClient):
    response = client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"