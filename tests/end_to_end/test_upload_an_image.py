import uuid
from pathlib import Path

import pytest
from fastapi import status

from app.schemas.image import ResponseUploadImage, ShiftArguments, UploadRequestBody

pytestmark = pytest.mark.asyncio

async def test_upload_an_image(http_client):
    """
    1. A user is created successfully.
    2. A user uploads an image.
    """
    external_id = str(uuid.uuid4())
    headers = {"X-External-User-ID": external_id}
    # --- CREATE A USER ---
    create_user_response = await http_client.post(url="/users-api/users", headers=headers)
    assert create_user_response.status_code == status.HTTP_201_CREATED
    create_user_response_json = create_user_response.json()
    # --- UPLOAD AN IMAGE ---
    image_path = Path("/image-augmentation-service/tests/data/test_image.png")
    assert image_path.exists()
    with open(image_path, "rb") as image_file:
        upload_response = await http_client.post(
            headers=headers,
            url="/image-api/upload/",
            files={"file": ("test.png", image_file, "image/png")},
        )
    assert upload_response.status_code == status.HTTP_200_OK
    ResponseUploadImage.model_validate(upload_response.json())