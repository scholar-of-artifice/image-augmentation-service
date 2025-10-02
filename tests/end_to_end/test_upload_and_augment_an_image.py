import io
import uuid
from pathlib import Path

import pytest
from fastapi import status
from PIL import Image, ImageChops

from app.schemas.image import ResponseUploadImage, ShiftArguments, UploadRequestBody, AugmentRequestBody, \
    RotateArguments

pytestmark = pytest.mark.asyncio

async def test_upload_and_augment_an_image(http_client):
    """
    1. A user is created successfully.
    2. A user uploads an image.
    3. A user then makes a request to `rotate` the image.
    """
    external_id = str(uuid.uuid4())
    headers = {"X-External-User-ID": external_id}
    # --- CREATE A USER ---
    create_user_response = await http_client.post(url="/users-api/users", headers=headers)
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
    upload_response_json = upload_response.json()
    # --- AUGMENT THE IMAGE ---
    augment_payload = {
        "unprocessed_image_id": upload_response_json["unprocessed_image_id"],
        "arguments": {
            "processing": "rotate",
            "angle": 45
        }
    }
    augment_response = await http_client.post(
        url="/image-api/augment/",
        json=augment_payload,
        headers=headers,
    )
    assert augment_response.status_code == status.HTTP_200_OK
    assert augment_response.json()["unprocessed_image_id"] == upload_response_json["unprocessed_image_id"]
    assert augment_response.json()["arguments"]["processing"] == "rotate"
    assert augment_response.json()["arguments"]["amount"] == 45