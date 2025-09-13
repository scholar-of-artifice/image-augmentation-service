from sqlmodel import Session
from app.schemas.transactions_db.user import User
from app.schemas.transactions_db.unprocessed_image import UnprocessedImage


def test_UnprocessedImage_creation_populates_user_relationship(db_session: Session):
    """
    GIVEN a User exists in the database
    AND a UnprocessedImage is created with that User.id
    WHEN the UnprocessedImage is committed.
    THEN the UnprocessedImage 'user' attribute is the correct User object.
    """
    # create a user
    user = User(external_id="some-1234-extr-0987-id45")
    # save the user
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="cool_image.png",
        storage_filename="some_file_name.png",
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
    user = User(external_id="some-1234-extr-0987-id45")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)  # Ensure we have the user's ID
    # create and unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="mountain_view-california.png",
        storage_filename="unique_storage_name.png",
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


def test_deleting_image_removes_it_from_user_list(db_session: Session):
    """
    GIVEN a User with one UnprocessedImage
    WHEN the UnprocessedImage is deleted from the database
    THEN the User's 'unprocessed_images' list becomes empty
    """
    # create a user with an unprocessed_image
    user = User(external_id="user-to-be-deleted-from")
    unprocessed_image = UnprocessedImage(
        user=user,
        original_filename="image_to_delete.jpg",
        storage_filename="storage_name_to_delete.jpg",
    )
    db_session.add(user)
    db_session.add(unprocessed_image)
    db_session.commit()
    db_session.refresh(user)
    # ensure this was saved correctly
    assert len(user.unprocessed_images) == 1
    # delete the image
    db_session.delete(unprocessed_image)
    db_session.commit()
    # refresh the user to get the latest state from the database
    db_session.refresh(user)
    # this user has an empty unprocessed_images list
    assert len(user.unprocessed_images) == 0


def test_deleting_user_cascades_to_delete_images(db_session: Session):
    """
    GIVEN a User with an UnprocessedImage
    WHEN the User is deleted
    THEN the associated UnprocessedImage is also deleted from the database
    """
    # create a user with an image
    user = User(external_id="cascading-delete-user")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="image_that_should_be_deleted.png",
        storage_filename="cascade_delete_storage.png",
    )
    db_session.add(unprocessed_image)
    db_session.commit()
    # store the ID to check for its existence later
    image_id = unprocessed_image.id
    # ensure the image is in the database
    assert db_session.get(UnprocessedImage, image_id) is not None
    # delete the user
    db_session.delete(user)
    db_session.commit()
    # the associated image should no longer exist in the database
    deleted_image = db_session.get(UnprocessedImage, image_id)
    assert deleted_image is None


def test_linking_by_parent_object_populates_foreign_key(db_session: Session):
    """
    GIVEN a User exists in the database
    WHEN an UnprocessedImage is created by assigning the User object directly
    to the 'user' relationship attribute
    THEN the 'user_id' foreign key field is automatically populated upon commit
    """
    # create a user
    user = User(external_id="user-for-object-linking")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    # create an image by assigning the parent object directly
    unprocessed_image = UnprocessedImage(
        original_filename="linked_by_object.png",
        storage_filename="storage_name_linked_by_object.png",
        user=user,  # Link via the relationship object, not the user_id
    )
    db_session.add(unprocessed_image)
    db_session.commit()
    # refresh the image to get its state from the database
    db_session.refresh(unprocessed_image)
    # the user_id foreign key should be correctly populated
    assert unprocessed_image.user_id is not None
    assert unprocessed_image.user_id == user.id
    # and the relationship should still be valid
    assert unprocessed_image.user.external_id == "user-for-object-linking"


def test_linking_by_appending_to_parent_list(db_session: Session):
    """
    GIVEN a User exists in the database
    WHEN a new UnprocessedImage is appended to the user.unprocessed_images list
    AND the session is committed
    THEN the image is saved and its 'user_id' foreign key is correctly set
    """
    # create a user that is already saved in the database
    user = User(external_id="user-for-list-append")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    # create a new unprocessed_images and append to the user's relationship list
    new_image = UnprocessedImage(
        original_filename="appended_image.jpg",
        storage_filename="storage_name_appended.jpg",
    )
    user.unprocessed_images.append(new_image)
    # add the user to the session again to register the change to the list
    db_session.add(user)
    db_session.commit()
    # refresh the user to load the newly added image from the DB
    db_session.refresh(user)
    # the image should be in the user's list and have the correct foreign key
    assert len(user.unprocessed_images) == 1
    image_from_db = user.unprocessed_images[0]
    assert image_from_db.user_id is not None
    assert image_from_db.user_id == user.id
    assert image_from_db.original_filename == "appended_image.jpg"


def test_deleting_image_does_not_delete_associated_user(db_session: Session):
    """
    GIVEN a User exists
    AND there is an associated UnprocessedImage
    WHEN the UnprocessedImage is deleted from the database
    THEN the User object remains in the database
    """
    # create a user with an image, both committed to the database
    user = User(external_id="user-who-should-survive")
    unprocessed_image = UnprocessedImage(
        user=user,
        original_filename="image_to_be_deleted.jpg",
        storage_filename="transient_image.jpg",
    )
    db_session.add(unprocessed_image)  # Adding the child cascades the add to the parent
    db_session.commit()
    # store IDs to query for them after the deletion
    user_id = user.id
    image_id = unprocessed_image.id
    # ensure both were committed
    assert db_session.get(User, user_id) is not None
    assert db_session.get(UnprocessedImage, image_id) is not None
    # delete the image
    db_session.delete(unprocessed_image)
    db_session.commit()
    # the image is gone, but the user remains
    image_in_db = db_session.get(UnprocessedImage, image_id)
    user_in_db = db_session.get(User, user_id)
    assert image_in_db is None
    assert user_in_db is not None
    # Verify it's the correct user
    assert user_in_db.id == user_id
    assert user_in_db.external_id == "user-who-should-survive"
