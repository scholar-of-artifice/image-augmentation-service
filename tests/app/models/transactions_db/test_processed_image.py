from sqlmodel import Session
from datetime import datetime, timezone
import os
from app.config import settings
from app.models.transactions_db.processed_image import ProcessedImage

def test_valid_processed_image_saves_expected_data(db_session: Session):
    """
        GIVEN a valid author_id ProcessedImage entry
        WHEN the entry is inserted into the database
        THEN it should have an id
        AND it should have the same author_id
        AND it should have the correct storage_filepath
        AND it should have a created_at with the correct format
    """
    image_to_create = ProcessedImage()

    db_session.add(image_to_create)
    db_session.commit()
    db_session.refresh(image_to_create)

    assert image_to_create.id is not None
    assert image_to_create.storage_filename != 'cool_image.png'
    assert image_to_create.storage_filepath == str(os.path.join(
        settings.PROCESSED_IMAGE_PATH, image_to_create.storage_filename
    ))
    assert isinstance(image_to_create.created_at, datetime)
    assert image_to_create.created_at.tzinfo == timezone.utc


