import uuid
from pathlib import Path
import pytest
from fastapi import status
from app.schemas.image import ResponseUploadImage

pytestmark = pytest.mark.asyncio

async def test_upload_an_image_201(http_client):
    """
    This test uploads a new image.
    1. Create a user
    2. Upload an image
    """
    external_id = str(uuid.uuid4())
    headers = {
        "X-External-User-ID": external_id
    }
    # --- CREATE A USER ---
    response = await http_client.post(
        url="/users-api/sign-up",
        headers=headers
    )
    # --- CHECK THE RESPONSE ---
    assert response.status_code == status.HTTP_201_CREATED
    create_user_response_json = response.json()
    # --- UPLOAD AN IMAGE ---
    image_path = Path("/image-augmentation-service/tests/data/test_image.png")
    assert image_path.exists()
    with open(image_path, "rb") as image_file:
        upload_response = await http_client.post(
            headers=headers,
            url="/image-api/upload",
            files={"image": ("test.png", image_file, "image/png")},
        )
    assert upload_response.status_code == status.HTTP_201_CREATED
    ResponseUploadImage.model_validate(upload_response.json())
