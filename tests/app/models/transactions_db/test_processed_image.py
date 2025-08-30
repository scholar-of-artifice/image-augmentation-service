from sqlmodel import Session
from datetime import datetime, timezone
from app.models.transactions_db.processed_image import ProcessedImage
from app.models.transactions_db.user import User
import uuid

def test_valid_processed_image_saves_expected_data(db_session: Session):
    """
        GIVEN a User exists in the database
        AND a valid ProcessedImage entry
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

    image_to_create = ProcessedImage(
        user_id= user_to_create.id,
        storage_filename='some_file_name.png',
    )

    db_session.add(image_to_create)
    db_session.commit()
    db_session.refresh(image_to_create)

    assert image_to_create.id is not None
    assert image_to_create.storage_filename == 'some_file_name.png'
    assert isinstance(image_to_create.created_at, datetime)
    assert image_to_create.created_at.tzinfo == timezone.utc


