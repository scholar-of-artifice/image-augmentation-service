import json
from fastapi import FastAPI, status
from pathlib import Path
from fastapi.testclient import TestClient
from app.routers.image import router
from app.models.image_api.upload import UploadRequestBody, ShiftArguments

app = FastAPI()
app.include_router(router)

client = TestClient(app)

TEST_DIR = Path(__file__).parent
TEST_IMAGES_PATH = TEST_DIR.parent.parent / "data" / "basic_shapes_250x250.png"

def test_upload_is_successful_when_request_is_valid():
    """
    GIVEN a valid image_file
    AND a valid request body
    WHEN .../upload is called
    THEN the request is successful
    """
    input_request_body = UploadRequestBody(arguments=ShiftArguments(processing="shift", direction="up", distance=2))
    with open(file=TEST_IMAGES_PATH, mode="rb") as image_file:
        response = client.post(url="/upload",
                               data={"body": input_request_body.model_dump_json()},
                               files={"file": ("basic_shapes_250x250.png", image_file, "image/png")}
                               )
        print(response.json())
        assert(response.status_code == status.HTTP_200_OK)


def test_upload_is_not_successful_when_request_uses_invalid_JSON():
    """
    GIVEN a valid image_file
    AND a bad request with invalid JSON
    WHEN .../upload is called
    THEN the request is not successful
    """
    input_request_body = {
        "arguments": {
            "processing": "shift",
            "direction": "left",
            "distance": 50
        }
    }
    input_request_str = json.dumps(input_request_body)
    input_request_str = input_request_str[:-5]
    with open(file=TEST_IMAGES_PATH, mode="rb") as image_file:
        response = client.post("/upload",
                               data={"body": input_request_str},
                               files={"file": ("basic_shapes_250x250.png", image_file, "image/png")}
                               )
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)

def test_upload_is_not_successful_when_request_uses_invalid_model():
    """
    GIVEN a valid image_file
    AND a bad request with invalid JSON
    WHEN .../upload is called
    THEN the request is not successful
    """
    input_request_body = {
        "arguments": {
            "processing": "rotate",
            "direction": "left",
            "distance": 50
        }
    }
    input_request_str = json.dumps(input_request_body)
    input_request_str = input_request_str[:-5]
    with open(file=TEST_IMAGES_PATH, mode="rb") as image_file:
        response = client.post("/upload",
                               data={"body": input_request_str},
                               files={"file": ("basic_shapes_250x250.png", image_file, "image/png")}
                               )
        assert(response.status_code == status.HTTP_400_BAD_REQUEST)


def test_upload_is_not_successful_when_request_uses_invalid_request_model():
    """
    GIVEN a valid image_file
    AND a bad request with invalid model
    WHEN .../upload is called
    THEN the request is not successful
    """
    input_request_body = {
        "arguments": {
            "processing": "rotate",
            "direction": "left",
            "distance": 50
        }
    }
    input_request_str = json.dumps(input_request_body)
    input_request_str = input_request_str[:-5]
    with open(file=TEST_IMAGES_PATH, mode="rb") as image_file:
        response = client.post("/upload",
                               data={"body": input_request_str},
                               files={"file": ("basic_shapes_250x250.png", image_file, "image/png")}
                               )
        assert(response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY)
