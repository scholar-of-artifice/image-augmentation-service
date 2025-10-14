from unittest.mock import AsyncMock
import io
import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import ValidationError
from pathlib import Path
from app.dependency.async_dependency import get_current_active_user
from app.main import app
from app.schemas.image import ResponseUploadImage, ShiftArguments, UploadRequestBody
from app.schemas.transactions_db import UnprocessedImage
from app.schemas.transactions_db.user import User
import uuid
from unittest.mock import patch

pytestmark = pytest.mark.asyncio

mock_user = User(id=uuid.uuid4(), external_id='test-user-123')

def override_get_current_active_user():
    return mock_user

app.dependency_overrides[get_current_active_user] = override_get_current_active_user

# --- upload_endpoint ---

async def test_upload_image_success(
    async_client: AsyncClient,
    async_db_session: AsyncSession,
):
    # save the user in the database
    async_db_session.add(mock_user)
    await async_db_session.flush()
    await async_db_session.refresh(mock_user)
    # create a byte stream.
    # simulate the content of a file.
    image_path = Path("/image-augmentation-service/tests/data/test_image.png")
    assert image_path.exists()
    # call the function
    with open(image_path, "rb") as image_file:
        # construct the post request
        headers = {"X-External-User-ID": mock_user.external_id}
        files = {'file': ("test_image.png", image_file, "image/png")}
        response = await async_client.post(
            url="/image-api/upload/",
            headers=headers,
            files=files
        )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data["unprocessed_image_id"], str)
    try:
        uuid.UUID(data["unprocessed_image_id"])
    except ValueError:
        pytest.fail(f"unprocessed_image_id: {data['unprocessed_image_id']} cannot be converted to UUID")
    assert isinstance(data["unprocessed_image_filename"], str)


# --- augment_endpoint ---

# --- get_unprocessed_image_by_id_endpoint ---

# --- get_processed_image_by_id_endpoint ---

# --- get_unprocessed_image_by_id_endpoint ---
