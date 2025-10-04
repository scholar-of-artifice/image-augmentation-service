
import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio

async def test_sign_up_a_user_401(http_client):
    """
    This test checks auth. is possible for creating a User.
    1. Create a user
    """
    external_id = ""
    headers = {
        "X-External-User-ID": external_id
    }
    # --- CREATE A USER ---
    response = await http_client.post(
        url="/users-api/sign-up",
        headers=headers
    )
    # --- CHECK THE RESPONSE ---
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
