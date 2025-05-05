from fastapi.testclient import TestClient

def test_get_roles(client: TestClient):
    # Assuming the /roles endpoint doesn't require authentication based on users.py
    response = client.get("/roles") # Adjust prefix if needed based on main.py include_router

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200 # Assuming StandardResponse format
    assert "details" in data
    assert isinstance(data["details"], list)
    # You might add more specific checks here if you know what roles should exist
    # For example, if you seed roles in your test setup:
    # assert any(role['name'] == 'Admin' for role in data['details'])