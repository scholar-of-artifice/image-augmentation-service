from sqlmodel import Session
from app.schemas.transactions_db.user import User
from app.services.user import get_user_by_external_id, create_user, delete_user
import uuid

# --- get_user_by_external_id ---
def test_get_user_by_external_id_found(mocker):
    """
        GIVEN an external_id that exists in the database
        AND a mock database session
        WHEN get_user_by_external_id is called
        THEN it returns the correct User object
    """
    # mock database session
    mock_session = mocker.MagicMock(spec=Session)
    # create sample user that the mock database will "return"
    sample_user = User(
        id="a-real-uuid",
        external_id="user-abc-123"
    )
    # configure the mock query chain to return the sample user
    mock_session.exec.return_value.first.return_value = sample_user
    # call the service function with the mock session
    result = get_user_by_external_id(
        db_session=mock_session,
        external_id="user-abc-123"
    )
    # check the results
    assert result is not None
    assert result.external_id == "user-abc-123"
    assert result == sample_user
    mock_session.exec.return_value.first.assert_called_once()

def test_get_user_by_external_id_not_found(mocker):
    """
        GIVEN an external_id that does not exist in the database
        AND a mock database session
        WHEN get_user_by_external_id is called
        THEN it returns None
    """
    # mock database session
    mock_session = mocker.MagicMock(spec=Session)
    # configure the mock query chain to return None
    mock_session.exec.return_value.first.return_value = None
    # call the function
    result = get_user_by_external_id(
        db_session=mock_session,
        external_id="user-does-not-exist"
    )
    # check the results
    assert result is None
    mock_session.exec.return_value.first.assert_called_once()

# --- create_user ---

def test_create_user(mocker):
    """
        GIVEN a valid external_id
        AND a mock database session
        WHEN create_user is called
        THEN it calls the session's add, commit, and refresh methods
        AND returns the newly created User object
    """
    # mock database session
    mock_session = mocker.MagicMock(spec=Session)
    # make input variable
    external_id = "new-user-456"
    # call the function
    new_user = create_user(
        db_session=mock_session,
        external_id=external_id
    )
    # check that a User object was created with the correct external_id
    assert isinstance(new_user, User)
    assert new_user.external_id == external_id
    # check that the correct database methods were called
    mock_session.add.assert_called_once_with(new_user)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(new_user)

# --- delete_user ---

def test_delete_user_success(mocker):
    """
        GIVEN an existing user ID
        AND the correct matching external_id for that user
        WHEN delete_user is called
        THEN the user is deleted and no exception is raised
    """
    # mock database session
    mock_session = mocker.MagicMock(spec=Session)
    # input variables
    user_id_to_delete = uuid.uuid4()
    correct_external_id = "owner-of-account-123"
    # create a user
    sample_user = User(id=user_id_to_delete, external_id=correct_external_id)
    # configure the mock query chain
    mock_session.get.return_value = sample_user
    # call the function
    delete_user(
        db_session=mock_session,
        user_id_to_delete=user_id_to_delete,
        requesting_external_id=correct_external_id,
    )
    # verify the correct methods were called in order
    mock_session.get.assert_called_once_with(User, user_id_to_delete)
    mock_session.delete.assert_called_once_with(sample_user)
    mock_session.commit.assert_called_once()