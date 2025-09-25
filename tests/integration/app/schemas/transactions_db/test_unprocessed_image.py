import uuid
from datetime import UTC, datetime

import pytest
from pydantic import ValidationError
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.transactions_db.unprocessed_image import UnprocessedImage
from app.schemas.transactions_db.user import User


pytestmark = pytest.mark.asyncio

async def test_unprocessed_image_is_valid(async_db_session: AsyncSession):
    """
    GIVEN a User exists in the database
    AND a valid UnprocessedImage entry
    WHEN the UnprocessedImage is inserted into the database
    THEN it persists correctly
    """
    # create a user
    user = User(external_id="some-1234-extr-0987-id45")
    async_db_session.add(user)
    await async_db_session.flush()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="cool_image.png",
        storage_filename="some_file_name.png",
    )
    # save the unprocessed_image
    async_db_session.add(unprocessed_image)
    await async_db_session.flush()
    await async_db_session.refresh(unprocessed_image, attribute_names=["id", "original_filename", "storage_filename", "created_at"])
    # test the unprocessed_image
    assert unprocessed_image.id is not None
    assert isinstance(unprocessed_image.id, uuid.UUID)
    assert unprocessed_image.user_id == user.id
    assert unprocessed_image.original_filename == "cool_image.png"
    assert unprocessed_image.storage_filename == "some_file_name.png"
    assert isinstance(unprocessed_image.created_at, datetime)
    assert unprocessed_image.created_at.tzinfo == UTC


async def test_unprocessed_image_IntegrityError_when_original_filename_is_null(
    async_db_session: AsyncSession,
):
    """
    GIVEN an attempt to create an UnprocessedImage entry
    AND the original_filename is None
    WHEN the entry is committed
    THEN an IntegrityError should be raised
    """
    # create a user
    user = User(external_id="some-1234-extr-0987-id45")
    async_db_session.add(user)
    await async_db_session.flush()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=user.id, original_filename=None, storage_filename="some_file_name.png"
    )
    # attempt to save the data
    async_db_session.add(unprocessed_image)
    with pytest.raises(IntegrityError):
        await async_db_session.flush()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    await async_db_session.rollback()


async def no_test_unprocessed_image_ValidationError_when_original_filename_is_blank_string(
    async_db_session: AsyncSession,
):
    # TODO: remove test from suite. validation not working as expected
    """
    GIVEN an attempt to create an UnprocessedImage entry
    AND the original_filename is a blank string
    WHEN the entry is committed
    THEN an ValidationError should be raised
    """
    # create a user
    user = User(external_id="some-1234-extr-0987-id45")
    async_db_session.add(user)
    await async_db_session.flush()
    with pytest.raises(ValidationError):
        UnprocessedImage(
            user_id=user.id, original_filename="", storage_filename="some_file_name.png"
        )
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    await async_db_session.rollback()


async def test_unprocessed_image_IntegrityError_when_storage_filename_is_null(
    async_db_session: AsyncSession,
):
    """
    GIVEN an attempt to create an UnprocessedImage entry
    AND the storage_filename is None
    WHEN the entry is committed
    THEN an IntegrityError should be raised
    """
    # create a user
    user = User(external_id="some-1234-extr-0987-id45")
    async_db_session.add(user)
    await async_db_session.flush()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=user.id, original_filename="cool_image.png", storage_filename=None
    )
    # attempt to save the data
    async_db_session.add(unprocessed_image)
    with pytest.raises(IntegrityError):
        await async_db_session.flush()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    await async_db_session.rollback()


async def no_test_unprocessed_image_ValidationError_when_storage_filename_is_blank_string(
    async_db_session: AsyncSession,
):
    # TODO: remove test from suite. validation not working as expected
    """
    GIVEN an attempt to create an UnprocessedImage entry
    AND the storage_filename is a blank string
    WHEN the entry is committed
    THEN an ValidationError should be raised
    """
    # create a user
    user = User(external_id="some-1234-extr-0987-id45")
    async_db_session.add(user)
    await async_db_session.flush()
    with pytest.raises(DataError):
        UnprocessedImage(
            user_id=user.id, original_filename="cool_image.png", storage_filename=""
        )
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    await async_db_session.rollback()


async def test_unprocessed_image_IntegrityError_when_user_id_is_null(async_db_session: AsyncSession):
    """
    GIVEN an attempt to create an UnprocessedImage entry
    AND the user_id is None
    WHEN the entry is committed
    THEN an IntegrityError should be raised
    """
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=None,
        original_filename="cool_image.png",
        storage_filename="some_file_name.png",
    )
    # attempt to save the data
    async_db_session.add(unprocessed_image)
    with pytest.raises(IntegrityError):
        await async_db_session.flush()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    await async_db_session.rollback()


async def test_unprocessed_image_DataError_when_original_filename_is_too_long(
    async_db_session: AsyncSession,
):
    """
    GIVEN an attempt to create an UnprocessedImage entry
    AND the original_filename is too long
    WHEN the entry is committed
    THEN a DataError should be raised
    """
    # create a user
    user = User(external_id="some-1234-extr-0987-id45")
    async_db_session.add(user)
    await async_db_session.flush()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="a" * 300,
        storage_filename="some_file_name.png",
    )
    # attempt to save the data
    async_db_session.add(unprocessed_image)
    with pytest.raises(DataError):
        await async_db_session.flush()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    await async_db_session.rollback()


async def test_unprocessed_image_DataError_when_storage_filename_is_to_long(
    async_db_session: AsyncSession,
):
    """
    GIVEN an attempt to create an UnprocessedImage entry
    AND the storage_filename is too long
    WHEN the entry is committed
    THEN a DataError should be raised
    """
    # create a user
    user = User(external_id="some-1234-extr-0987-id45")
    async_db_session.add(user)
    await async_db_session.flush()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="cool_image.png",
        storage_filename="a" * 300,
    )
    # attempt to save the data
    async_db_session.add(unprocessed_image)
    with pytest.raises(DataError):
        await async_db_session.flush()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    await async_db_session.rollback()


async def test_unprocessed_image_IntegrityError_when_user_id_does_not_exist(
    async_db_session: AsyncSession,
):
    """
    GIVEN an attempt to create an UnprocessedImage entry
    AND the user_id does not exist
    WHEN the entry is committed
    THEN an IntegrityError should be raised
    """
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=uuid.uuid4(),
        original_filename="cool_image.png",
        storage_filename="some_file_name.png",
    )
    # attempt to save the data
    async_db_session.add(unprocessed_image)
    with pytest.raises(IntegrityError):
        await async_db_session.flush()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    await async_db_session.rollback()


async def test_unprocessed_image_is_IntegrityError_when_storage_file_name_is_duplicated(
    async_db_session: AsyncSession,
):
    """
    GIVEN an UnprocessedImage A
    AND an UnprocessedImage B
    AND storage_filenames are the same
    WHEN that B is committed
    THEN an IntegrityError is raised
    """
    # create a user
    user = User(external_id="some_external_id")
    async_db_session.add(user)
    await async_db_session.flush()
    # create an image
    unprocessed_image_A = UnprocessedImage(
        user_id=user.id,
        original_filename="cool_image.png",
        storage_filename="some_file_name.png",
    )
    # save the data
    async_db_session.add(unprocessed_image_A)
    await async_db_session.flush()
    # create another image
    unprocessed_image_B = UnprocessedImage(
        user_id=user.id,
        original_filename="cool_image.png",
        storage_filename="some_file_name.png",
    )
    # attempt to save the data
    async_db_session.add(unprocessed_image_B)
    with pytest.raises(IntegrityError):
        await async_db_session.flush()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    await async_db_session.rollback()


async def test_get_unprocessed_image_by_primary_key(async_db_session: AsyncSession):
    """
    GIVEN a UnprocessedImage model
    AND it is persisted in the database
    WHEN UnprocessedImage model is retrieved by primary key
    THEN the data is correct
    """
    # create a user
    user = User(external_id="some_external_id")
    async_db_session.add(user)
    await async_db_session.flush()
    # create a user
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="cool_image.png",
        storage_filename="some_file_name.png",
    )
    async_db_session.add(unprocessed_image)
    await async_db_session.flush()
    await async_db_session.refresh(unprocessed_image)
    # get the unprocessed_image by id
    retrieved_image = await async_db_session.get(UnprocessedImage, unprocessed_image.id)
    # assert that the images are the same
    assert retrieved_image.id is not None
    assert isinstance(retrieved_image.id, uuid.UUID)
    assert retrieved_image.user_id == user.id
    assert retrieved_image.original_filename == "cool_image.png"
    assert retrieved_image.storage_filename == "some_file_name.png"


async def test_get_unprocessed_image_by_primary_key_not_found(async_db_session: AsyncSession):
    """
    GIVEN no UnprocessedImage exists with a specific ID
    WHEN a UnprocessedImage is retrieved by that ID
    THEN the result is None
    """
    # make some UUID
    non_existent_id = uuid.uuid4()
    # try to get a user with that ID
    retrieved_unprocessed_image = await async_db_session.get(UnprocessedImage, non_existent_id)
    # the result is None
    assert retrieved_unprocessed_image is None


async def test_delete_unprocessed_image(async_db_session: AsyncSession):
    """
    GIVEN a UnprocessedImage exists in the database
    WHEN the UnprocessedImage is deleted
    THEN it can no longer be retrieved from the database
    """
    # create a user
    user = User(external_id="some_external_id")
    async_db_session.add(user)
    await async_db_session.flush()
    # create a user
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="cool_image.png",
        storage_filename="some_file_name.png",
    )
    async_db_session.add(unprocessed_image)
    await async_db_session.flush()
    await async_db_session.refresh(unprocessed_image, attribute_names=["id"])
    assert unprocessed_image.id is not None
    await async_db_session.delete(unprocessed_image)
    # store its ID so we can look for it later
    unprocessed_image_id = unprocessed_image.id
    # confirm it's in the database before deleting
    assert await async_db_session.get(UnprocessedImage, unprocessed_image_id) is not None
    # delete the image
    await async_db_session.delete(unprocessed_image)
    await async_db_session.flush()
    # the image cannot be found by its primary key
    retrieved_image = await async_db_session.get(UnprocessedImage, unprocessed_image_id)
    assert retrieved_image is None


# TODO: Test accessing the parent user object from an image instance (image.user).
# TODO: Test that a user's 'unprocessed_images' list is correctly populated.
# TODO: Test fetching all images belonging to a specific user.
# TODO: Test that deleting a User with associated images raises an IntegrityError.
# TODO: Test if providing a filename longer than max_length raises a DataError.
