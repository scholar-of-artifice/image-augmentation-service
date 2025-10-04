
import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio

async def test_sign_up_a_user_401(http_client):
    """
    GIVEN an invalid external_id
    WHEN a request is made to sign-up
    THEN a 401 response is returned

    1. Create a user
    """
    bad_external_id = ""
    headers = {
        "X-External-User-ID": bad_external_id
    }
    # --- CREATE A USER ---
    response = await http_client.post(
        url="/users-api/sign-up",
        headers=headers
    )
    # --- CHECK THE RESPONSE ---
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
