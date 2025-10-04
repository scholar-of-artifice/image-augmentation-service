import uuid

import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio

async def test_delete_a_user_204(http_client):
    """
    GIVEN a user A
    WHEN A requests to delete A
    THEN a 403 is returned

    1. Sign up a user A
    3. A requests to delete A
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
    # --- DELETE A USER ---
    response = await http_client.delete(
        url=f"/users-api/user/{response_A.json()['id']}",
        headers=headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
