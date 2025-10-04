import uuid

import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio

async def test_delete_a_user_404(http_client):
    """
    This test deletes a user that does not exist.
    1. Delete a user
    """
    external_id = str(uuid.uuid4())
    headers = {
        "X-External-User-ID": external_id
    }
    # --- DELETE A USER ---
    response = await http_client.delete(
        url=f"/users-api/user/{str(uuid.uuid4())}",
        headers=headers
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
