import pytest
from fastapi import HTTPException, status
from sqlmodel import Session
from app.schemas.transactions_db.user import User
from app.dependency.sync_dependency import get_current_active_user

# --- get_current_active_user ---

def test_get_current_active_user_success(mocker):
    """
        GIVEN a valid external_id for an existing user
        AND a mock database session that finds the user
        WHEN get_current_active_user is called
        THEN it returns the correct User model object
    """
    # GIVEN
    sample_user = User(id="a-real-uuid", external_id="user-abc-123")
    # create a mock session using the mocker fixture
    mock_session = mocker.MagicMock(spec=Session)
    # configure the mock to simulate the query chain
    mock_session.exec.return_value.first.return_value = sample_user
    # call the function
    found_user = get_current_active_user(
        external_id="user-abc-123",
        db_session=mock_session
    )
    # check the output
    assert found_user == sample_user
    mock_session.exec.return_value.first.assert_called_once()

def test_get_current_active_user_raises_not_found_when_user_does_not_exist(mocker):
    """
        GIVEN a valid external_id for a non-existent user
        AND a mock database session that does not find the user
        WHEN get_current_active_user is called
        THEN it raises an HTTPException with a 404 status
    """
    # create a mock session using the mocker fixture
    mock_session = mocker.MagicMock(spec=Session)
    # configure the mock to return None, simulating a user not found
    mock_session.exec.return_value.first.return_value = None
    # call the function
    with pytest.raises(HTTPException) as exc:
        get_current_active_user(
            external_id="user-that-does-not-exist",
            db_session=mock_session
        )
        # check the output
        assert exc.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc.value.detail == "User not found."
        mock_session.exec.return_value.first.assert_called_once()