from app.routers.user import router
from fastapi.testclient import TestClient

def test_create_user_success(client: TestClient):
    """
        GIVEN an external_user_id
        WHEN the POST request is made to create a new user
        THEN check the response is valid
    """
    # define the header for a new, unique user
    headers = {
        "X-External-User-ID": "new-user-123"
    }
    # make the POST request to the endpoint
    response = client.post(
        url="/users-api/users",
        headers=headers
    )
    # check the results
    assert response.status_code == 201
    data = response.json()
    assert data["external_id"] == "new-user-123"
    assert "id" in data
    assert data["id"] is not None
    assert "created_at" in data
    assert data["created_at"] is not None