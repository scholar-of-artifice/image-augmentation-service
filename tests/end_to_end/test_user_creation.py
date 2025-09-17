import httpx
import os
import uuid
import pytest
from fastapi import status

BASE_URL = os.getenv("API_BASE_URL")
USER_ENDPOINT_PATH = "/users-api/users"

def test_user_create_a_user():
    """
    GIVEN a valid set of parameters
    WHEN the POST request is made to the endpoint
    THEN the response is successful
    """
    assert BASE_URL, "API_BASE_URL environment variable is not set"
    external_id = str(uuid.uuid4())
    headers = {"X-External-User-ID": external_id}
    with httpx.Client() as client:
        response = client.post(url=f"{BASE_URL}{USER_ENDPOINT_PATH}", headers=headers)
    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()
    assert response_json["external_id"] == external_id
    assert "id" in response_json
    assert "created_at" in response_json
    # validate the format of the internal UUID
    try:
        uuid.UUID(response_json["id"])
    except ValueError:
        pytest.fail(f"The returned id {response_json['id']} was not a valid UUID")
