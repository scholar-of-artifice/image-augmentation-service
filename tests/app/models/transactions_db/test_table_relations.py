from sqlmodel import Session
from app.models.transactions_db.user import User
from app.models.transactions_db.unprocessed_image import UnprocessedImage

# TODO: write a test which enforces the relationship between User and UnprocessedImage

# TODO: write a test which enforces the relationship between User and ProcessedImage

# TODO: write a test which enforces the relationship between UnprocessedImage and ProcessedImage

# TODO: write a test which enforces the relationship between ProcessingJob and User

# TODO: write a test which enforces the relationship between ProcessingJob and UnprocessedImage

# TODO: write a test which enforces the relationship between ProcessingJob and ProcessedImage

def test_UnprocessedImage_creation_populates_user_relationship(db_session: Session):
    """
        GIVEN a User exists in the database
        AND a UnprocessedImage is created with that User.id
        WHEN the UnprocessedImage is committed.
        THEN the UnprocessedImage 'user' attribute is the correct User object.
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45')
    # save the user
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
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
    # Assert that the ORM relationship attribute has been populated
    assert unprocessed_image.user is not None
    assert isinstance(unprocessed_image.user, User)
    # Assert that it's the correct user by comparing primary keys and another unique field
    assert unprocessed_image.user.id == user.id
    assert unprocessed_image.user.external_id == user.external_id

def test_user_image_list_is_updated_after_image_creation(db_session: Session):
    """
        GIVEN a User exists
        AND an UnprocessedImage is created for that user
        WHEN the User object is refreshed from the database
        THEN the 'unprocessed_images' list should contain the new image
    """
    # create a user
    user = User(external_id='some-1234-extr-0987-id45')
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user) # Ensure we have the user's ID
    # create and unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="mountain_view-california.png",
        storage_filename="unique_storage_name.png"
    )
    db_session.add(unprocessed_image)
    db_session.commit()
    # refresh to see what was written in db
    db_session.refresh(user)
    # is relationship list is populated correctly?
    assert user.unprocessed_images is not None
    assert len(user.unprocessed_images) == 1
    # verify the image in the list is the right one
    image_from_list = user.unprocessed_images[0]
    assert isinstance(image_from_list, UnprocessedImage)
    assert image_from_list.id == unprocessed_image.id
    assert image_from_list.storage_filename == "unique_storage_name.png"

# TODO: Test linking by assigning the parent object directly, instead of using the foreign key ID.

# TODO: Test linking by appending an image to the user's list of images.

# --- TODOs for Constraint & Deletion Violations ---

# TODO: Test that the foreign key constraint prevents creating an image with a fake user_id.

# TODO: Test that the database prevents a user from being deleted if they still have images.

# TODO: Test that deleting an image does not affect its parent user.
