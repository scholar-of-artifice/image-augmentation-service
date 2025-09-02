from app.routers.user import router
from fastapi.testclient import TestClient
from fastapi import status

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
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["external_id"] == "new-user-123"
    assert "id" in data
    assert data["id"] is not None
    assert "created_at" in data
    assert data["created_at"] is not None

def test_create_user_raises_conflict_when_user_already_exists(client: TestClient):
    """
        GIVEN an external_id
        AND a user with the same external_id already exists
        WHEN the POST request is made to create a new user
        THEN it returns 409
    """
    # create a user
    headers = {
        "X-External-User-ID": "existing-user-456"
    }
    response = client.post("/users-api/users", headers=headers)
    # this first call should succeed
    assert response.status_code == status.HTTP_201_CREATED
    # attempt to create the same user again
    response = client.post("/users-api/users", headers=headers)
    # check for the conflict error
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": "User with external_id 'existing-user-456' already exists."
    }

def test_create_user_raises_unauthorized_when_user_is_not_authorized(client: TestClient):
    """
        GIVEN an external_id
        AND a user with the same external_id already exists
        WHEN the POST request is made to create a new user
        THEN it returns 401
    """
    # create a user
    headers = {
        "X-External-User-ID": ""
    }
    # make the request
    response = client.post("/users-api/users", headers=headers)
    # check the failure
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Missing X-External-User-ID header'}