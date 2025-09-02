import pytest
import uuid
from fastapi import HTTPException, status
from app.dependency import get_current_external_user_id

pytestmark = pytest.mark.asyncio

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

async def test_get_current_external_user_id_success_when_external_id_is_present():
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