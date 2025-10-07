import uuid
from unittest.mock import AsyncMock, MagicMock
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.transactions_db.user import User
from app.schemas.user import ResponseSignUpUser
from app.services.user import (
    sign_up_user_service,
    delete_user_service,
    sign_up_user_service,
)
import app.exceptions as exc

pytestmark = pytest.mark.asyncio

# --- sign_up_user_service ---


async def test_sign_up_user_service(mocker):
    """
    GIVEN a new external_id not in the database
    WHEN the sign_up_user_service is called
    THEN it should create and return a new user.
    """
    # make input variable
    test_external_id = "new-user-123"
    test_user_id = uuid.uuid4()
    mock_session = AsyncMock(spec=AsyncSession)
    # mock the repository layer response when checking for an existing user
    mock_get_user = mocker.patch(
        "app.services.user.repository_layer.get_user_by_external_id",
        return_value=None
    )
    mock_create_unprocessed_directory = mocker.patch(
        "app.services.user.create_unprocessed_user_directory",
        return_value=None
    )
    mock_create_processed_directory = mocker.patch(
        "app.services.user.create_processed_user_directory",
        return_value=None
    )
    # mock the User object that the repository create_user function would return
    mock_created_user = MagicMock()
    mock_created_user.id = test_user_id
    mock_created_user.external_id = test_external_id
    # mock the repository layer response when creating the user
    mock_create_user = mocker.patch(
        "app.services.user.repository_layer.create_user",
        return_value=mock_created_user
    )
    # call the function
    result = await sign_up_user_service(
        external_id=test_external_id,
        db_session=mock_session
    )
    # check that we tried to find an existing user
    mock_get_user.assert_awaited_once_with(
        external_id=test_external_id,
        db_session=mock_session
    )
    # check that we created a new user since one did not exist
    mock_create_user.assert_awaited_once_with(
        external_id=test_external_id,
        db_session=mock_session
    )
    mock_create_unprocessed_directory.assert_awaited_once_with(
        user_id=test_user_id,
    )
    mock_create_processed_directory.assert_awaited_once_with(
        user_id=test_user_id,
    )
    # check that the final result is correct
    assert isinstance(result, ResponseSignUpUser)
    assert result.id == test_user_id
    assert result.external_id == test_external_id


# --- delete_user_service ---


async def test_delete_user_service_success(mocker):
    """
    GIVEN an existing user ID
    AND the correct matching external_id for that user
    WHEN delete_user is called
    THEN the user is deleted and no exception is raised
    """
    # mock database session
    mock_session = AsyncMock(spec=AsyncSession)

    # input variables
    user_id_to_delete = uuid.uuid4()
    correct_external_id = "owner-of-account-123"
    # create a user
    sample_user = User(id=user_id_to_delete, external_id=correct_external_id)
    # configure the mock query chain
    mock_session.get.return_value = sample_user
    # call the function
    await delete_user_service(
        db_session=mock_session,
        user_id_to_delete=user_id_to_delete,
        external_id=correct_external_id,
    )
    # verify the correct methods were called in order
    mock_session.get.assert_awaited_once_with(User, user_id_to_delete)
    mock_session.delete.assert_called_once_with(sample_user)
    mock_session.commit.assert_awaited_once()


async def test_delete_user_service_raises_user_not_found(mocker):
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
    with pytest.raises(exc.UserNotFound):
        await delete_user_service(
            db_session=mock_session,
            user_id_to_delete=non_existent_user_id,
            external_id="any-external-id",
        )
    # verify that the delete and commit methods were NOT called
    mock_session.delete.assert_not_awaited()
    mock_session.commit.assert_not_awaited()


async def test_delete_user_service_raises_permission_denied(mocker):
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
    with pytest.raises(exc.PermissionDenied):
        await delete_user_service(
            db_session=mock_session,
            user_id_to_delete=user_id_to_delete,
            external_id=incorrect_external_id,
        )
    # verify that the delete and commit methods were NOT called
    mock_session.delete.assert_not_awaited()
    mock_session.commit.assert_not_awaited()
