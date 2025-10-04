import uuid

import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio

async def test_sign_up_same_user_409(http_client):
    """
    This test checks the same user cannot be created multiple times.
    1. Create a user A
    2. Create a user A again
    """
    external_id = str(uuid.uuid4())
    headers = {
        "X-External-User-ID": external_id
    }
    # --- CREATE A USER ---
    response = await http_client.post(
        url="/users-api/sign-up",
        headers=headers
    )
    # --- CHECK THE RESPONSE ---
    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()
    assert response_json["external_id"] == external_id
    try:
        uuid.UUID(response_json["id"])
    except ValueError:
        pytest.fail(f"The returned id {response_json['id']} was not a valid UUID")
    # --- CREATE THE USER AGAIN ---
    response = await http_client.post(
        url="/users-api/sign-up",
        headers=headers
    )
    # --- CHECK THE RESPONSE ---
    assert response.status_code == status.HTTP_409_CONFLICT
