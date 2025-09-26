import uuid
from pathlib import Path

import pytest
from fastapi import status

from app.schemas.image import ShiftArguments, UploadRequestBody, ImageProcessResponse
import fnmatch

pytestmark = pytest.mark.asyncio

async def test_upload_an_image_to_shift(http_client):
    """
    This test creates a user and then allows that user to upload an image.
    1. A user is created successfully.
    2. A user uploads an image with a request to `shift` it.
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
    shift_args = ShiftArguments(processing="shift", direction="right", distance=25)
    request_body = UploadRequestBody(arguments=shift_args)
    with open(image_path, "rb") as image_file:
        upload_response = await http_client.post(
            headers=headers,
            url="/image-api/upload/",
            files={"file": ("test.png", image_file, "image/png")},
            data={"body": request_body.model_dump_json()},
        )
    assert upload_response.status_code == status.HTTP_200_OK
    ImageProcessResponse.model_validate(upload_response.json())