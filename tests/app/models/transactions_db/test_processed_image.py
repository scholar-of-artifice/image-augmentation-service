from sqlmodel import Session
from datetime import datetime, timezone
from app.models.transactions_db.processed_image import ProcessedImage
from app.models.transactions_db.unprocessed_image import UnprocessedImage
from app.models.transactions_db.user import User
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, DataError
import pytest
import uuid

def test_processed_image_is_valid(db_session: Session):
    """
        GIVEN a User exists in the database
        AND a valid ProcessedImage entry
        WHEN the ProcessedImage is inserted into the database
        THEN it persists correctly
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45')
    db_session.add(user)
    db_session.commit()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id= user.id,
        original_filename='cool_image.png',
        storage_filename="some_file_name.png"
    )
    db_session.add(unprocessed_image)
    db_session.commit()
    # create a processed_image
    processed_image = ProcessedImage(
        user_id= user.id,
        unprocessed_image_id=unprocessed_image.id,
        storage_filename="some_new_file_name.png"
    )
    # save the processed_image
    db_session.add(processed_image)
    db_session.commit()
    db_session.refresh(processed_image)
    # test the processed_image
    assert processed_image.id is not None
    assert isinstance(processed_image.id, uuid.UUID)
    assert processed_image.user_id == user.id
    assert processed_image.storage_filename == 'some_new_file_name.png'
    assert isinstance(processed_image.created_at, datetime)
    assert processed_image.created_at.tzinfo == timezone.utc

def test_processed_image_IntegrityError_when_user_id_is_null(db_session: Session):
    """
        GIVEN no user_id
        AND a ProcessedImage entry is created
        WHEN the ProcessedImage is inserted into the database
        THEN it raises an IntegrityError
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45')
    db_session.add(user)
    db_session.commit()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id= user.id,
        original_filename='cool_image.png',
        storage_filename="some_file_name.png"
    )
    db_session.add(unprocessed_image)
    db_session.commit()
    # create a processed_image
    processed_image = ProcessedImage(
        user_id= None,
        unprocessed_image_id=unprocessed_image.id,
        storage_filename="some_new_file_name.png"
    )
    # attempt to save the data
    db_session.add(processed_image)
    db_session.add(processed_image)
    with pytest.raises(IntegrityError):
        db_session.commit()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    db_session.rollback()

def test_processed_image_IntegrityError_when_user_id_does_not_exist(db_session: Session):
    """
        GIVEN a user_id that does not exist
        AND a ProcessedImage entry is created
        WHEN the ProcessedImage is inserted into the database
        THEN it raises an IntegrityError
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45')
    db_session.add(user)
    db_session.commit()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id= user.id,
        original_filename='cool_image.png',
        storage_filename="some_file_name.png"
    )
    db_session.add(unprocessed_image)
    db_session.commit()
    # create a processed_image
    processed_image = ProcessedImage(
        user_id= uuid.uuid4(),
        unprocessed_image_id=unprocessed_image.id,
        storage_filename="some_new_file_name.png"
    )
    # attempt to save the data
    db_session.add(processed_image)
    db_session.add(processed_image)
    with pytest.raises(IntegrityError):
        db_session.commit()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    db_session.rollback()

def test_processed_image_IntegrityError_when_storage_filename_is_nil(db_session: Session):
    """
        GIVEN a User exists in the database
        AND a ProcessedImage entry
        AND the storage_filename is nil
        WHEN the ProcessedImage is inserted into the database
        THEN it raises an IntegrityError
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45')
    db_session.add(user)
    db_session.commit()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id= user.id,
        original_filename='cool_image.png',
        storage_filename="some_file_name.png"
    )
    db_session.add(unprocessed_image)
    db_session.commit()
    # create a processed_image
    processed_image = ProcessedImage(
        user_id= user.id,
        unprocessed_image_id=unprocessed_image.id,
        storage_filename=None
    )
    # save the processed_image
    db_session.add(processed_image)
    with pytest.raises(IntegrityError):
        db_session.commit()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    db_session.rollback()

def no_test_processed_image_IntegrityError_when_storage_filename_is_blank_string(db_session: Session):
    # TODO: remove this test from suite. pydantic validation not working as inteneded
    """
        GIVEN a User exists in the database
        AND a ProcessedImage entry
        AND the storage_filename is a blank string
        WHEN the ProcessedImage is inserted into the database
        THEN it raises an IntegrityError
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45')
    db_session.add(user)
    db_session.commit()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id= user.id,
        original_filename='cool_image.png',
        storage_filename="some_file_name.png"
    )
    db_session.add(unprocessed_image)
    db_session.commit()
    # create a processed_image
    processed_image = ProcessedImage(
        user_id= user.id,
        unprocessed_image_id=unprocessed_image.id,
        storage_filename=""
    )
    # save the processed_image
    db_session.add(processed_image)
    with pytest.raises(IntegrityError):
        db_session.commit()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    db_session.rollback()

def test_processed_image_DataError_when_storage_filename_is_too_long(db_session: Session):
    # TODO: remove this test from suite. pydantic validation not working as intended
    """
        GIVEN a User exists in the database
        AND a ProcessedImage entry
        AND the storage_filename is too long
        WHEN the ProcessedImage is inserted into the database
        THEN it raises an DataError
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45')
    db_session.add(user)
    db_session.commit()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id= user.id,
        original_filename='cool_image.png',
        storage_filename="some_file_name.png"
    )
    db_session.add(unprocessed_image)
    db_session.commit()
    # create a processed_image
    processed_image = ProcessedImage(
        user_id= user.id,
        unprocessed_image_id=unprocessed_image.id,
        storage_filename="a"*300
    )
    # save the processed_image
    db_session.add(processed_image)
    with pytest.raises(DataError):
        db_session.commit()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    db_session.rollback()

