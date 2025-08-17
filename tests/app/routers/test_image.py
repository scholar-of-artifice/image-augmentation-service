import json
from fastapi import FastAPI
from pathlib import Path
from fastapi.testclient import TestClient
from app.routers.image import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)

TEST_DIR = Path(__file__).parent
TEST_IMAGES_PATH = TEST_DIR.parent.parent / "data" / "basic_shapes_250x250.png"

def test_upload_is_successful_when_request_is_valid_shift():
    """
    GIVEN a valid image_file
    WHEN .../upload is called
    THEN the request is successful
    """
    input_request_body = {
        "arguments": {
            "processing": "shift",
            "direction": "left",
            "distance": 50
        }
    }
    with open(file=TEST_IMAGES_PATH, mode="rb") as image_file:
        response = client.post("/upload",
                               data={"body": json.dumps(input_request_body)},
                               files={"file": ("basic_shapes_250x250.png", image_file, "image/png")}
                               )
        response_json = response.json()
        assert(response.status_code == 200)
        # TODO: should i assert this?
        #  assert(response_json["output_file_path"] == 'app/_tmp/[some_file_name].png')
