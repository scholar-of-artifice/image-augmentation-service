import pytest
import json
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from tests.app.helperfunc.helperfunc import get_test_image
from app.routers.image import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_upload_with_bad_request_body_returns_unprocessable_entity():
    """
        GIVEN the endpoint /upload
        AND an image
        AND a bad request body
        WHEN a request is made
        THEN an exception is thrown
    """
    try:
        # this is the image
        with get_test_image() as image_bytes:
            # this is a bad set of arguments
            json_body = json.dumps({
                "arguments": {
                    "processing": "rotate",
                    "distance": 20
                }
            })
            response = client.post(
                url="/upload",
                data={"body": json_body},
                files={"file": ("test.png", image_bytes, "image/png")},
            )
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    except (FileNotFoundError, ValueError) as e:
        pytest.fail(f"Failed to load test image: {e}")

def test_upload_with_invalid_json_returns_bad_request():
    """
        GIVEN the endpoint /upload
        AND an image
        AND a bad request body with invalid json
        WHEN a request is made
        THEN an exception is thrown
    """
    try:
        # this is the image
        with get_test_image() as image_bytes:
            # this is a bad set of arguments
            json_body = json.dumps({
                "arguments": {
                    "processing": "rotate",
                    "distance": 20
                }
            })
            response = client.post(
                url="/upload",
                data={"body": json_body[:-10]},
                files={"file": ("test.png", image_bytes, "image/png")},
            )
            assert response.status_code == status.HTTP_400_BAD_REQUEST
    except (FileNotFoundError, ValueError) as e:
        pytest.fail(f"Failed to load test image: {e}")
