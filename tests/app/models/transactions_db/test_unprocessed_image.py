from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
import pytest
import uuid
from app.models.transactions_db.unprocessed_image import UnprocessedImage
from app.models.transactions_db.user import User

def test_valid_unprocessed_image_saves_expected_data(db_session: Session):
    """
        GIVEN a User exists in the database
        AND a valid UnprocessedImage entry
        WHEN the entry is inserted into the database
        THEN it should have an id
        AND it should have the same user_id
        AND it should have the same original_filename
        AND it should have the correct storage_filepath
        AND it should have a created_at with the correct format
    """
    user_to_create = User(external_id='some-1234-extr-0987-id45', name="Test User")
    db_session.add(user_to_create)
    db_session.commit()

    image_to_create = UnprocessedImage(
        user_id= user_to_create.id,
        original_filename= "cool_image.png",
        storage_filename="some_file_name.png"
    )

    db_session.add(image_to_create)
    db_session.commit()
    db_session.refresh(image_to_create)

    assert image_to_create.id is not None
    assert image_to_create.user_id == user_to_create.id
    assert image_to_create.original_filename == 'cool_image.png'
    assert image_to_create.storage_filename == 'some_file_name.png'
    assert isinstance(image_to_create.created_at, datetime)
    assert image_to_create.created_at.tzinfo == timezone.utc

def test_create_image_fails_when_user_does_not_exist(db_session: Session):
    """
        GIVEN an attempt to create an UnprocessedImage entry
        WHEN the user_id does not exist
        THEN an IntegrityError should be raised upon commit
    """

    image_with_bad_original_filename = UnprocessedImage(
        user_id= uuid.uuid4(),
        original_filename= "cool_image.png",
        storage_filename="some_file_name.png"
    )
    db_session.add(image_with_bad_original_filename)
    # Use pytest.raises as a context manager to catch the expected error
    with pytest.raises(IntegrityError):
        db_session.commit() # The error will be raised here

def test_create_image_fails_when_storage_file_name_is_duplicated(db_session: Session):
    """
        GIVEN a UnprocessedImage model
        AND storage_filename is duplicated
        WHEN that model is potentially persisted
        THEN there are is an error
    """
    user_to_create = User(external_id='some-1234-extr-0987-id45', name="Test User")
    db_session.add(user_to_create)
    db_session.commit()

    image_A = UnprocessedImage(
        user_id= user_to_create.id,
        original_filename= "cool_image.png",
        storage_filename="some_file_name.png"
    )
    # Create the first image successfully
    db_session.add(image_A)
    db_session.commit()

    image_B = UnprocessedImage(
        user_id= user_to_create.id,
        original_filename= "cool_image.png",
        storage_filename="some_file_name.png"
    )

    # Create a second user with the same external_id
    db_session.add(image_B)

    # Assert that committing this change raises an IntegrityError
    # This is how we test for database constraint violations
    with pytest.raises(IntegrityError):
        db_session.commit()