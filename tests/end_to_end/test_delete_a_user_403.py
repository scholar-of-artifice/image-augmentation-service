import uuid

import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio

async def test_delete_a_user_403(http_client):
    """
    GIVEN a user A
    AND a user B
    WHEN B requests to delete A
    THEN a 403 si returned

    1. Sign up a user A
    2. Sign up a user B
    3. B requests to delete A
    """
    # --- CREATE A USER ---
    external_id_A = str(uuid.uuid4())
    headers = {
        "X-External-User-ID": external_id_A
    }
    response_A = await http_client.post(
        url="/users-api/sign-up",
        headers=headers
    )
    assert response_A.status_code == status.HTTP_201_CREATED
    # --- CREATE A USER ---
    external_id_B = str(uuid.uuid4())
    headers = {
        "X-External-User-ID": external_id_B
    }
    response_B = await http_client.post(
        url="/users-api/sign-up",
        headers=headers
    )
    assert response_B.status_code == status.HTTP_201_CREATED
    # --- DELETE A USER ---
    response = await http_client.delete(
        url=f"/users-api/user/{response_A.json()['id']}",
        headers=headers
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
