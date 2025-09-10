from sqlmodel import Session
from app.schemas.transactions_db.user import User
from app.services.user import get_user_by_external_id

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
        db=mock_session, external_id="user-abc-123"
    )
    # check the results
    assert result is not None
    assert result.external_id == "user-abc-123"
    assert result == sample_user
    mock_session.exec.return_value.first.assert_called_once()

# --- create_user ---