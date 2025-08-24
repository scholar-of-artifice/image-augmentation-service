import numpy as np
import pytest
import json
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from tests.app.helperfunc.helperfunc import get_test_image
from app.routers.image import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)


def test_upload_with_good_request_body_returns_success(mocker):
    """
        GIVEN the endpoint /upload
        AND an image
        AND a request body
        WHEN a request is made
        THEN the response is successfully returned
    """
    # TODO: explain what is mocked
    mock_translate = mocker.patch('app.routers.image.translate_file_to_numpy_array')
    mock_write_original = mocker.patch('app.routers.image.write_numpy_array_to_image_file')
    mock_rotate = mocker.patch('app.routers.image.rotate')
    mock_write_new = mocker.patch('app.routers.image.write_numpy_array_to_image_file')
    mock_create_filename = mocker.patch('app.routers.image.create_file_name')

    mock_translate.return_value = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    mock_rotate.return_value = np.array([[9, 8 ,7], [6, 5, 4], [3, 2, 1]])
    mock_create_filename.return_value = "some_file_name.png"

    try:
        # this is the image
        with get_test_image() as image_bytes:
            # this is a bad set of arguments
            json_body = json.dumps({
                "arguments": {
                    "processing": "rotate",
                    "angle": 45
                }
            })
            response = client.post(
                url="/upload",
                data={"body": json_body},
                files={"file": ("test.png", image_bytes, "image/png")},
            )
            assert response.status_code == status.HTTP_200_OK
    except (FileNotFoundError, ValueError) as e:
        pytest.fail(f"Failed to load test image: {e}")

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
