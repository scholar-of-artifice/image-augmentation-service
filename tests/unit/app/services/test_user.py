import uuid
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.transactions_db.user import User
from app.services.user import (
    PermissionDenied,
    UserNotFound,
    create_user,
    delete_user,
    get_user_by_external_id,
)

pytestmark = pytest.mark.asyncio

# --- get_user_by_external_id ---
async def test_get_user_by_external_id_found(mocker):
    """
    GIVEN an external_id that exists in the database
    AND a mock database session
    WHEN get_user_by_external_id is called
    THEN it returns the correct User object
    """
    # mock database session
    mock_session = AsyncMock(spec=AsyncSession)
    # create sample user that the mock database will "return"
    sample_user = User(id="a-real-uuid", external_id="user-abc-123")
    # configure the mock query chain to return the sample user
    mock_result = mocker.MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.first.return_value = sample_user
    # call the service function with the mock session
    result = await get_user_by_external_id(
        db_session=mock_session, external_id="user-abc-123"
    )
    # check the results
    assert result is not None
    assert result.external_id == "user-abc-123"
    assert result == sample_user
    mock_session.execute.assert_awaited_once()


async def test_get_user_by_external_id_not_found(mocker):
    """
    GIVEN an external_id that does not exist in the database
    AND a mock database session
    WHEN get_user_by_external_id is called
    THEN it returns None
    """
    # mock database session
    mock_session = AsyncMock(spec=AsyncSession)
    # configure the mock query chain to return None
    mock_result = mocker.MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_result.scalars.return_value.first.return_value = None
    # call the function
    result = await get_user_by_external_id(
        db_session=mock_session, external_id="user-does-not-exist"
    )
    # check the results
    assert result is None
    mock_session.execute.assert_awaited_once()


# --- create_user ---


async def test_create_user(mocker):
    """
    GIVEN a valid external_id
    AND a mock database session
    WHEN create_user is called
    THEN it calls the session's add, commit, and refresh methods
    AND returns the newly created User object
    """
    # mock database session
    mock_session = AsyncMock(spec=AsyncSession)
    # make input variable
    external_id = "new-user-456"
    # call the function
    new_user = await create_user(db_session=mock_session, external_id=external_id)
    # check that a User object was created with the correct external_id
    assert isinstance(new_user, User)
    assert new_user.external_id == external_id
    # check that the correct database methods were called
    mock_session.add.assert_called_once_with(new_user)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(new_user)


# --- delete_user ---


async def test_delete_user_success(mocker):
    """
    GIVEN an existing user ID
    AND the correct matching external_id for that user
    WHEN delete_user is called
    THEN the user is deleted and no exception is raised
    """
    # mock database session
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session = AsyncMock(spec=AsyncSession)

    # input variables
    user_id_to_delete = uuid.uuid4()
    correct_external_id = "owner-of-account-123"
    # create a user
    sample_user = User(id=user_id_to_delete, external_id=correct_external_id)
    # configure the mock query chain
    mock_session.get.return_value = sample_user
    # call the function
    await delete_user(
        db_session=mock_session,
        user_id_to_delete=user_id_to_delete,
        requesting_external_id=correct_external_id,
    )
    # verify the correct methods were called in order
    mock_session.get.assert_awaited_once_with(User, user_id_to_delete)
    mock_session.delete.assert_called_once_with(sample_user)
    mock_session.commit.assert_awaited_once()


async def test_delete_user_raises_user_not_found(mocker):
    """
    GIVEN a user_id that does not exist
    WHEN delete_user is called
    THEN a UserNotFound exception is raised
    """
    # mock database session
    mock_session = AsyncMock(spec=AsyncSession)
    # input variables
    non_existent_user_id = uuid.uuid4()
    # configure the mock query chain
    mock_session.get.return_value = None
    # call the function
    with pytest.raises(UserNotFound):
        await delete_user(
            db_session=mock_session,
            user_id_to_delete=non_existent_user_id,
            requesting_external_id="any-external-id",
        )
    # verify that the delete and commit methods were NOT called
    mock_session.delete.assert_not_awaited()
    mock_session.commit.assert_not_awaited()


async def test_delete_user_raises_permission_denied(mocker):
    """
    GIVEN an existing user's ID
    AND an external_id that does NOT match the user's external_id
    WHEN delete_user is called
    THEN a PermissionDenied exception is raised
    """
    # mock database session
    mock_session = AsyncMock(spec=AsyncSession)
    # input variables
    user_id_to_delete = uuid.uuid4()
    correct_external_id = "owner-of-account-123"
    incorrect_external_id = "not-the-owner-456"
    sample_user = User(id=user_id_to_delete, external_id=correct_external_id)
    # configure the mock query chain
    mock_session.get.return_value = sample_user
    # call the funciton
    with pytest.raises(PermissionDenied):
        await delete_user(
            db_session=mock_session,
            user_id_to_delete=user_id_to_delete,
            requesting_external_id=incorrect_external_id,
        )
    # verify that the delete and commit methods were NOT called
    mock_session.delete.assert_not_awaited()
    mock_session.commit.assert_not_awaited()

# --- overhauled service layer API ---

# --- create_UnprocessedImage_entry ---

# --- read_UnprocessedImage_entry ---

# --- create_ProcessedImage_entry ---

# --- read_ProcessedImage_entry ---
