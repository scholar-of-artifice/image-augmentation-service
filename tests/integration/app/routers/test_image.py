import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI, status
from app.main import app
from app.schemas.transactions_db.user import User
from app.dependency.async_dependency import get_current_active_user
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.schemas.image import ImageProcessResponse, ShiftArguments, UploadRequestBody
from app.routers.image import router

pytestmark = pytest.mark.asyncio

async def test_upload_endpoint_success(mocker, async_client):
    """
        GIVEN a valid file
        AND a valid request body
        WHEN a POST request is made to /upload
        THEN a 200 OK response is returned
    """
    # define a fake user and a simple override function
    fake_user = User(id=1, external_id="fake-test-user-id")
    async def override_get_current_active_user():
        return fake_user
    # apply the override to the main app object
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    # Use a try...finally block to ensure cleanup
    try:
        # input values
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
        response = await async_client.post(
            url="/image-api/upload/",
            files={"file": ('test.png', b'fake_image_bytes', 'image/png')},
            data={'body': request_body.model_dump_json()}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response.model_dump()
        mocked_service.assert_called_once
    finally:
        # this will always run and ensure a clean state
        app.dependency_overrides.clear()

async def test_upload_endpoint_missing_body_fails_with_422(mocker, async_client):
    """
        GIVEN a file is provided
        BUT the request body is missing
        WHEN a POST request is made to /upload
        THEN a 422 Unprocessable Entity response is returned
    """
    # define a fake user and a simple override function
    fake_user = User(id=1, external_id="fake-test-user-id")
    async def override_get_current_active_user():
        return fake_user
    # apply the override to the main app object
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    # Use a try...finally block to ensure cleanup
    try:
        # input values
        # We don't need to mock the service because the request should fail
        # validation before the service is ever called.

        # Note the missing 'data' parameter in the request
        response = await async_client.post(
            url="/image-api/upload/",
            files={"file": ('test.png', b'fake_image_bytes', 'image/png')},
        )
        # Assert that FastAPI caught the missing data and returned a 422
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    finally:
        # this will always run and ensure a clean state
        app.dependency_overrides.clear()
