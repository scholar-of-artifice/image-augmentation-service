from sqlmodel import Session
from datetime import datetime
import uuid
from app.models.transactions_db.user import User

def test_create_user_is_successful(db_session: Session):
    """
        GIVEN a User model
        AND all input data is valid
        WHEN that model is persisted
        THEN there are no errors
        AND the data is correct
    """
    user_to_create = User(external_id='some-1234-extr-0987-id45', name="Test User")

    db_session.add(user_to_create)
    db_session.commit()
    db_session.refresh(user_to_create)

    # Assert that the database populated the fields correctly
    assert user_to_create.id is not None
    assert isinstance(user_to_create.id, uuid.UUID)
    assert user_to_create.external_id == 'some-1234-extr-0987-id45'
    assert user_to_create.created_at is not None
    assert isinstance(user_to_create.created_at, datetime)
    # Check that the timezone info was correctly stored
    assert user_to_create.created_at.tzinfo is not None