from sqlmodel import Session
from app.schemas.transactions_db.user import User
from app.dependency.async_dependency import get_current_active_user

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