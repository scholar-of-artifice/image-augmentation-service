import uuid
from pathlib import Path

import pytest
from fastapi import status

from app.schemas.image import ShiftArguments, UploadRequestBody, ImageProcessResponse

pytestmark = pytest.mark.asyncio

async def test_upload_and_download_an_unprocessed_image(http_client):
    """
    This test creates a user and then allows that user to upload an image.
    It then downloads that image.
    1. A user is created successfully.
    2. A user uploads an image with a request to `shift` it.
    2. A user downloads the original unprocessed image.
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
    unprocessed_image_content = None
    with open(image_path, "rb") as image_file:
        unprocessed_image_content = image_file.read()
        image_file.seek(0)
        upload_response = await http_client.post(
            headers=headers,
            url="/image-api/upload/",
            files={"file": ("test.png", image_file, "image/png")},
            data={"body": request_body.model_dump_json()},
        )
    assert upload_response.status_code == status.HTTP_200_OK
    ImageProcessResponse.model_validate(upload_response.json())
    # --- DOWNLOAD THE UNPROCESSED IMAGE ---
    unprocessed_image_id = upload_response.json()["unprocessed_image_id"]
    print(upload_response.json())
    download_response = await http_client.get(
        headers=headers,
        url=f"/image-api/unprocessed-image/{unprocessed_image_id}/"
    )
    assert download_response.status_code == status.HTTP_200_OK
    assert unprocessed_image_content == download_response.content()