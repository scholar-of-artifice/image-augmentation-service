from sqlmodel import Session
from sqlalchemy.exc import DataError
from datetime import datetime, timezone
import pytest
import os
from app.config import settings
from app.models.transactions_db.unprocessed_image import UnprocessedImage

def test_valid_unprocessed_image_saves_expected_data(db_session: Session):
    """
        GIVEN a valid author_id UnprocessedImage entry
        WHEN the entry is inserted into the database
        THEN it should have an id
        AND it should have the same author_id
        AND it should have the same original_filename
        AND it should have the correct storage_filepath
        AND it should have a created_at with the correct format
    """
    image_to_create = UnprocessedImage(
        author_id= 101,
        original_filename= "cool_image.png",
    )

    db_session.add(image_to_create)
    db_session.commit()
    db_session.refresh(image_to_create)

    assert image_to_create.id is not None
    assert image_to_create.author_id == 101
    assert image_to_create.original_filename == 'cool_image.png'
    assert image_to_create.storage_filename != 'cool_image.png'
    assert image_to_create.storage_filepath == str(os.path.join(
        settings.UNPROCESSED_IMAGE_PATH, image_to_create.storage_filename
    ))
    assert isinstance(image_to_create.created_at, datetime)
    assert image_to_create.created_at.tzinfo == timezone.utc

def test_create_image_with_string_author_id_fails(db_session: Session):
    """
        GIVEN an attempt to create an UnprocessedImage entry
        WHEN the author_id is a string instead of an integer
        THEN an IntegrityError should be raised upon commit
    """

    image_with_bad_id = UnprocessedImage(
        author_id="this-is-not-an-integer",  # Invalid data type
        original_filename="test.jpg",
    )
    # Use pytest.raises as a context manager to catch the expected error
    with pytest.raises(DataError):
        db_session.add(image_with_bad_id)
        db_session.commit() # The error will be raised here

