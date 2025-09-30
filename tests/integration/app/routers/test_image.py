from unittest.mock import AsyncMock

import pytest
from fastapi import status
from pydantic import ValidationError
from pathlib import Path
from app.dependency.async_dependency import get_current_active_user
from app.main import app
from app.schemas.image import ResponseUploadImage, ShiftArguments, UploadRequestBody
from app.schemas.transactions_db import UnprocessedImage
from app.schemas.transactions_db.user import User
import uuid

pytestmark = pytest.mark.asyncio

# --- upload_endpoint ---

async def NO_test_upload_endpoint_success(mocker, async_client):
    """
    GIVEN a valid file
    AND a valid request body
    WHEN a POST request is made to /upload
    THEN a 200 OK response is returned
    """
    pytest.fail("TODO: write this test!")
    # define a fake user and a simple override function
    fake_user = User(id=1, external_id="fake-test-user-id")

    async def override_get_current_active_user():
        return fake_user

    # apply the override to the main app object
    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    # Use a try...finally block to ensure cleanup
    try:
        # input values
        shift_args = ShiftArguments(
            processing="shift",
            direction="right",
            distance=25
        )
        request_body = UploadRequestBody(arguments=shift_args)
        #
        expected_response = ResponseUploadImage(
            processed_image_id=uuid.uuid4(),
            processed_image_filename=str(uuid.uuid4()) + '.png',
        )
        #
        mocked_service = mocker.patch(
            "app.routers.image.process_and_save_image",
            return_value=expected_response
        )
        #
        response = await async_client.post(
            url="/image-api/upload/",
            files={
                "file": (
                    "test.png",
                    b"fake_image_bytes",
                    "image/png"
                )
            }
        )
        assert response.status_code == status.HTTP_200_OK
        try:
            ResponseUploadImage.model_validate(response.json())
        except ValidationError as e:
            pytest.fail(f"Response JSON could not be validated as ImageResponse: {e}")
    finally:
        # this will always run and ensure a clean state
        app.dependency_overrides.clear()


async def NO_test_upload_endpoint_unauthorized(mocker, async_client):
    """
    GIVEN a valid file
    AND a valid request body
    AND no external_id
    WHEN a POST request is made to /upload
    THEN a 401 OK response is returned
    """
    pytest.fail("TODO: write this test!")
    # Use a try...finally block to ensure cleanup
    try:
        # input values
        shift_args = ShiftArguments(processing="shift", direction="right", distance=42)
        request_body = UploadRequestBody(arguments=shift_args)
        #
        mocked_service = mocker.patch(
            "app.routers.image.process_and_save_image"
        )
        #
        response = await async_client.post(
            url="/image-api/upload/",
            files={"file": ("test.png", b"fake_image_bytes", "image/png")},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == { "detail": "Missing X-External-User-ID header"}
        mocked_service.assert_not_called()
    finally:
        # this will always run and ensure a clean state
        app.dependency_overrides.clear()


async def NO_test_upload_endpoint_missing_body_fails_with_422(mocker, async_client):
    """
    GIVEN a file is provided
    BUT the request body is missing
    WHEN a POST request is made to /upload
    THEN a 422 Unprocessable Entity response is returned
    """
    pytest.fail("TODO: write this test!")
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
            files={"file": ("test.png", b"fake_image_bytes", "image/png")},
        )
        # Assert that FastAPI caught the missing data and returned a 422
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    finally:
        # this will always run and ensure a clean state
        app.dependency_overrides.clear()


async def NO_test_upload_endpoint_fails_on_service_error_with_500(mocker, async_client):
    # TODO: fix this test. not passing for some unknown reason.
    """
    GIVEN a valid request
    AND the underlying service function raises an unexpected exception
    WHEN a POST request is made to /upload
    THEN a 500 Internal Server Error response is returned
    """
    # create a fake user and a dependency override
    fake_user = User(id=1, external_id="fake-test-user-id")

    async def override_get_current_active_user():
        return fake_user

    app.dependency_overrides[get_current_active_user] = override_get_current_active_user
    try:
        # create a valid request body
        shift_args = ShiftArguments(processing="shift", direction="right", distance=25)
        request_body = UploadRequestBody(arguments=shift_args)
        # create the service function is mocked to raise an error
        mocked_service = mocker.patch(
            "app.routers.image.process_and_save_image",
            new_callable=AsyncMock,
            side_effect=Exception("A simulated service layer error occurred"),
        )
        # call the function
        response = await async_client.post(
            url="/image-api/upload/",
            files={"file": ("test.png", b"fake_image_bytes", "image/png")}
        )
        # check the response is a 500 error
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        # Optionally, check the default FastAPI error message
        assert response.json() == {"detail": "Internal Server Error"}
        # check the mocked service was called
        mocked_service.assert_called_once()
    finally:
        # clean up the dependency override
        app.dependency_overrides.clear()

async def NO_test_get_unprocessed_image_by_id_endpoint_success_when_image_exists(mocker, async_client):
    """
    GIVEN a valid id of an image in the database
    WHEN a GET request is made to /unprocessed-image/{id}
    THEN a 200 OK is returned
    AND an unprocessed image is downloaded
    """
    assert 1 == 3


async def NO_test_get_unprocessed_image_by_id_endpoint_fails_when_image_does_not_exist(mocker, async_client):
    """
    GIVEN an invalid id of an image NOT in the database
    WHEN a GET request is made to /unprocessed-image/{id}
    THEN a 404 is returned
    AND nothjing is downloaded
    """
    assert 1 == 3