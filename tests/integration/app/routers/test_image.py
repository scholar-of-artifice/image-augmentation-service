import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from app.schemas.image import ImageProcessResponse, ShiftArguments, UploadRequestBody
from app.routers.image import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

pytestmark = pytest.mark.asyncio

async def test_upload_endpoint_success(mocker):
    """
        GIVEN a valid file
        AND a valid request body
        WHEN a POST request is made to /upload
        THEN a 200 OK response is returned
    """
    shift_args = ShiftArguments(processing='shift', direction='right', distance=25)
    request_body = UploadRequestBody(arguments=shift_args)
    #
    expected_response = ImageProcessResponse(
        original_stored_file_path="mock/orginal.png",
        new_stored_file_path="mock/new.png",
        body=request_body
    )
    #
    mocked_service = mocker.patch(
        'app.routers.image.process_and_save_image',
        return_value=expected_response
    )
    #
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            url="/upload/",
            files={"file": ('test.png', b'fake_image_byetes', 'image/png')},
            data={'body': request_body.model_dump_json()}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response.model_dump()
        mocked_service.assert_called_once

async def test_upload_endpoint_missing_body_fails_with_422(mocker):
    """
        GIVEN a file is provided
        BUT the request body is missing
        WHEN a POST request is made to /upload
        THEN a 422 Unprocessable Entity response is returned
    """
    # We don't need to mock the service because the request should fail
    # validation before the service is ever called.

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Note the missing 'data' parameter in the request
        response = await ac.post(
            url="/upload/",
            files={"file": ('test.png', b'fake_image_bytes', 'image/png')},
        )
        # Assert that FastAPI caught the missing data and returned a 422
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_upload_endpoint_service_error_fails_with_500(mocker):
    """
        GIVEN a valid file and request body
        BUT the image processing service raises an unexpected error
        WHEN a POST request is made to /upload
        THEN a 500 Internal Server Error response is returned
    """
    shift_args = ShiftArguments(processing='shift', direction='right', distance=25)
    request_body = UploadRequestBody(arguments=shift_args)
    # mock the service function to raise an exception instead of returning a value
    mocked_service = mocker.patch(
        'app.routers.image.process_and_save_image',
        side_effect=OSError("Something went wrong with saving the file")
    )
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        response = await ac.post(
            url="/upload/",
            files={"file": ('test.png', b'fake_image_bytes', 'image/png')},
            data={'body': request_body.model_dump_json()}
        )
        # assert that the endpoint handled the service error correctly
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        # check the content of the error message
        assert response.json() == {"detail": "Internal Server Error"}
        mocked_service.assert_called_once()