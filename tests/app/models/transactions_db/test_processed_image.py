from sqlmodel import Session
from datetime import datetime, timezone
from app.models.transactions_db.processed_image import ProcessedImage
from app.models.transactions_db.user import User
import uuid

def test_processed_image_is_valid(db_session: Session):
    """
        GIVEN a User exists in the database
        AND a valid ProcessedImage entry
        WHEN the ProcessedImage is inserted into the database
        THEN it persists correctly
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45', name="Test User")
    db_session.add(user)
    db_session.commit()
    # create an unprocessed_image
    processed_image = ProcessedImage(
        user_id= user.id,
        storage_filename="some_file_name.png"
    )
    # save the processed_image
    db_session.add(processed_image)
    db_session.commit()
    db_session.refresh(processed_image)
    # test the processed_image
    assert processed_image.id is not None
    assert isinstance(processed_image.id, uuid.UUID)
    assert processed_image.user_id == user.id
    assert processed_image.storage_filename == 'some_file_name.png'
    assert isinstance(processed_image.created_at, datetime)
    assert processed_image.created_at.tzinfo == timezone.utc


