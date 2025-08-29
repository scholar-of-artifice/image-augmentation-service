from sqlmodel import Session
from datetime import datetime, timezone
import uuid
from sqlalchemy.exc import IntegrityError
from app.models.transactions_db.user import User
import pytest

def test_user_valid_model_is_persisted(db_session: Session):
    """
        GIVEN a User model
        AND all input data is valid
        WHEN that model is persisted
        THEN there are no errors
        AND the data is correct
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45')
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    # Assert that the database populated the fields correctly
    assert isinstance(user.id, uuid.UUID)
    assert user.id is not None
    assert user.external_id == 'some-1234-extr-0987-id45'
    assert user.external_id is not None
    assert isinstance(user.created_at, datetime)
    assert user.created_at is not None
    assert user.created_at.tzinfo is not None
    assert user.created_at.tzinfo == timezone.utc

def test_user_IntegrityError_when_external_id_is_duplicate(db_session: Session):
    """
        GIVEN a User A already exists
        AND a new User B is created
        AND both Users have the same external ID
        WHEN User B model is committed
        THEN an IntegrityError is raised
    """
    # create 2 users with same external_id
    user_A = User(external_id='some-1234-extr-0987-id45')
    user_B = User(external_id='some-1234-extr-0987-id45')
    # commit only the first user
    db_session.add(user_A)
    db_session.commit()
    # attempt to commit the second user
    db_session.add(user_B)
    with pytest.raises(IntegrityError):
        db_session.commit()

def test_user_IntegrityError_when_external_id_is_null(db_session: Session):
    """
        GIVEN a User model
        AND external_id is null
        WHEN that model is potentially persisted
        THEN there are is an errors
    """
    user_to_create = User(external_id=None)

    # Create the first user successfully
    db_session.add(user_to_create)

    # Assert that committing this change raises an IntegrityError
    # This is how we test for database constraint violations
    with pytest.raises(IntegrityError):
        db_session.commit()

# TODO: Test fetching a user by their primary key (id).
# TODO: Test fetching a user by their unique external_id.
# TODO: Test that querying for a non-existent user returns None.
# TODO: Test updating a user's attribute (e.g., a new 'display_name' field).
# TODO: Test that read-only fields like 'id' and 'created_at' are not changed on commit.
# TODO: Test deleting a user and verifying it's no longer in the database.
# TODO: Test what happens when trying to delete a user that doesn't exist.
# TODO: Test creating a user with an empty string for external_id.
# TODO: Test how the database handles an external_id that is unusually long.
# TODO: Test querying with an invalid UUID format to ensure it fails gracefully.
