import pytest
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