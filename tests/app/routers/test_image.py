import json
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.routers.image import router
from app.models.image_api.upload import UploadRequestBody, ProcessingEnum, RotateArguments

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_upload_is_successful_when_request_is_valid():
    # TODO: make request body
    json_data = {
        "processing": "rotate",
        "arguments": {
            "amount": 10
        }
    }
    response = client.post(
        url="/upload/",
        json=json_data
    )
    assert response.status_code == 200
    assert response.json() == {"filename": 'file.filename',
                               "message": "Image processed successfully."}
