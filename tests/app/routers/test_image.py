import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.image import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_upload_is_successful_when_request_is_valid():
    # TODO: make request body
    json_data = {
        "arguments": {
            "processing": "rotate",
            "amount": 10
        }
    }
    dummy_files = {
        "file": ("test_image.jpg", b"dummy image content", "image/jpeg")
    }
    response = client.post(
        url="/upload/",
        data={"body": json.dumps(json_data)},
        files=dummy_files
    )
    assert response.status_code == 200
    assert response.json() == {"filename": "test_image.jpg",
                               "message": "Image processed successfully."}
