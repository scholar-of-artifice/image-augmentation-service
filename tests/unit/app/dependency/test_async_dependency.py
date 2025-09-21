import json
import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependency.async_dependency import (
    get_body_as_model,
    get_current_active_user,
    get_current_external_user_id,
)
from app.schemas.image import RotateArguments, UploadRequestBody
from app.schemas.transactions_db.user import User

pytestmark = pytest.mark.asyncio

# --- get_current_external_user_id ---


async def test_get_current_external_user_id_success_when_external_id_is_present():
    """
    GIVEN an external_id is in the header
    WHEN get_current_external_user_id is called
    THEN it returns the external_id
    """
    # define a sample external ID.
    test_external_id = "user-abc-123"
    # call the dependency function directly, passing the test ID.
    result = await get_current_external_user_id(external_id=test_external_id)
    # check that the returned value is what we expect.
    assert result == test_external_id


async def test_get_current_external_user_id_success_when_realistic_external_id_is_present():
    """
    GIVEN a user_id is in the header
    AND external_id is a more realistic example
    WHEN get_current_external_user_id
    THEN it returns the user_id
    """
    # define a sample external ID.
    test_external_id = str(uuid.uuid4())
    # call the dependency function directly, passing the test ID.
    result = await get_current_external_user_id(external_id=test_external_id)
    # check that the returned value is what we expect.
    assert result == test_external_id


async def test_get_current_external_user_id_raise_HTTPException_when_external_id_is_not_present():
    """
    GIVEN a user_id is not in the header
    WHEN get_current_external_user_id
    THEN it raises an HTTPException
    AND has particular details
    """
    # define a sample external ID.
    test_external_id = None
    with pytest.raises(HTTPException) as exc:
        # call the dependency function directly, passing the test ID.
        await get_current_external_user_id(external_id=test_external_id)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Missing X-External-User-ID header" in str(exc.value.detail)


async def test_get_current_external_user_id_raise_HTTPException_when_external_id_is_a_blank_string():
    """
    GIVEN a user_id is a blank string
    WHEN get_current_external_user_id
    THEN it raises an HTTPException
    AND has particular details
    """
    # define a sample external ID.
    test_external_id = ""
    with pytest.raises(HTTPException) as exc:
        # call the dependency function directly, passing the test ID.
        await get_current_external_user_id(external_id=test_external_id)
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Missing X-External-User-ID header" in str(exc.value.detail)


# get_body_as_model


async def test_get_body_as_model_returns_correct_body():
    """
    GIVEN the input body is a valid request
    WHEN get_body_as_model is called
    THEN it returns the correct model
    AND it raises no exceptions
    """
    valid_model_string = json.dumps(
        {"arguments": {"processing": "rotate", "angle": 20}}
    )
    expected_result = UploadRequestBody(
        arguments=RotateArguments(processing="rotate", angle=20)
    )
    calculated_result = await get_body_as_model(body=valid_model_string)
    assert calculated_result == expected_result


async def test_get_body_as_model_raises_unprocessable_entity_when_not_valid_json():
    """
    GIVEN the input body is not a valid json string
    WHEN get_body_as_model is called
    THEN it raises an unprocessable entity exception
    """
    not_a_valid_json_string = "not_a_valid_json_string"
    with pytest.raises(HTTPException) as exc:
        await get_body_as_model(body=not_a_valid_json_string)
    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_get_body_as_model_raises_unprocessable_entity_when_model_not_correct():
    """
    GIVEN the input body is not a valid model
    WHEN get_body_as_model is called
    THEN it raises an unprocessable entity exception
    """
    valid_json_string = json.dumps({"foo": "bar"})
    with pytest.raises(HTTPException) as exc:
        await get_body_as_model(body=valid_json_string)
    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert isinstance(exc.value.detail, list)
    assert len(exc.value.detail) > 0


async def test_get_current_active_user_success(mocker):
    """
    GIVEN a valid external_id for an existing user
    AND a mock database session that finds the user
    WHEN get_current_active_user is called
    THEN it returns the correct User model object
    """
    # create a sample user
    sample_user = User(id="a-real-uuid", external_id="user-abc-123")
    # create a mock database session
    mock_session = mocker.MagicMock(spec=AsyncSession)
    # configure the mock to simulate the ASYNCHRONOUS query chain
    # the .first() method now returns an awaitable object (the AsyncMock)
    mock_result = mocker.MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.first.return_value = sample_user
    # the async function is awaited
    found_user = await get_current_active_user(
        external_id="user-abc-123", db_session=mock_session
    )
    # the output is correct and the mock was awaited
    assert found_user == sample_user
    mock_session.execute.assert_awaited_once()


async def test_get_current_active_user_raises_not_found_when_user_does_not_exist(
    mocker,
):
    """
    GIVEN a valid external_id for a non-existent user
    AND a mock database session that does not find the user
    WHEN get_current_active_user is called
    THEN it raises an HTTPException with a 404 status
    """
    # create a mock session
    mock_session = mocker.MagicMock(spec=AsyncSession)
    # configure the mock to return an awaitable that resolves to None
    mock_result = mocker.MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.first.return_value = None
    # the function is awaited inside the pytest.raises context
    with pytest.raises(HTTPException) as exc:
        await get_current_active_user(
            external_id="user-that-does-not-exist", db_session=mock_session
        )
    # check the correct exception is raised and the mock was awaited
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == "User not found."
    mock_session.execute.assert_awaited_once()
