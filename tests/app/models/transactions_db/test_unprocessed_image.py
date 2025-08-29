from sqlmodel import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
import pytest
import uuid
from app.models.transactions_db.unprocessed_image import UnprocessedImage
from app.models.transactions_db.user import User

def test_unprocessed_image_is_valid(db_session: Session):
    """
        GIVEN a User exists in the database
        AND a valid UnprocessedImage entry
        WHEN the UnprocessedImage is inserted into the database
        THEN it persists correctly
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45', name="Test User")
    db_session.add(user)
    db_session.commit()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id= user.id,
        original_filename= "cool_image.png",
        storage_filename="some_file_name.png"
    )
    # save the unprocessed_image
    db_session.add(unprocessed_image)
    db_session.commit()
    db_session.refresh(unprocessed_image)
    # test the unprocessed_image
    assert unprocessed_image.id is not None
    assert isinstance(unprocessed_image.id, uuid.UUID)
    assert unprocessed_image.user_id == user.id
    assert unprocessed_image.original_filename == 'cool_image.png'
    assert unprocessed_image.storage_filename == 'some_file_name.png'
    assert isinstance(unprocessed_image.created_at, datetime)
    assert unprocessed_image.created_at.tzinfo == timezone.utc

def test_unprocessed_image_IntegrityError_when_user_id_does_not_exist(db_session: Session):
    """
        GIVEN an attempt to create an UnprocessedImage entry
        AND the user_id does not exist
        WHEN the entry is committed
        THEN an IntegrityError should be raised
    """
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id= uuid.uuid4(),
        original_filename= "cool_image.png",
        storage_filename="some_file_name.png"
    )
    # attempt to save the data
    db_session.add(unprocessed_image)
    with pytest.raises(IntegrityError):
        db_session.commit()

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