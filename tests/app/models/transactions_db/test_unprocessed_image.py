from sqlmodel import Session
from app.models.transactions_db.unprocessed_image import UnprocessedImage

def test_create_unprocessed_image_is_successful(db_session: Session):
    """
        Tests that a valid UnprocessedImage can be created and saved.
    """
    # Arrange: Create a new image instance
    image_to_create = UnprocessedImage(
        author_id=101,
        original_filename="cool_image.png",
        storage_filename="abc-123.png",
        storage_filepath="/path/to/storage/abc-123.png",
    )

    # Act: Add to the session and commit
    db_session.add(image_to_create)
    db_session.commit()
    db_session.refresh(image_to_create)

    # Assert: Check that the object was saved and has an ID
    assert image_to_create.id is not None
    assert image_to_create.author_id == 101
    assert image_to_create.created_at is not None

    # Assert: Query the database to confirm it exists
    retrieved_image = db_session.get(UnprocessedImage, image_to_create.id)
    assert retrieved_image is not None
    assert retrieved_image.storage_filename == "abc-123.jpg"