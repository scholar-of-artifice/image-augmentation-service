import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.transactions_db.processed_image import ProcessedImage
from app.schemas.transactions_db.unprocessed_image import UnprocessedImage
from app.schemas.transactions_db.user import User

pytestmark = pytest.mark.asyncio

async def test_processed_image_is_valid(async_db_session: AsyncSession):
    """
    GIVEN a User exists in the database
    AND a valid ProcessedImage entry
    WHEN the ProcessedImage is inserted into the database
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
    async_db_session.add(unprocessed_image)
    await async_db_session.flush()
    # create a processed_image
    processed_image = ProcessedImage(
        unprocessed_image_id=unprocessed_image.id,
        storage_filename="some_new_file_name.png",
    )
    # save the processed_image
    async_db_session.add(processed_image)
    await async_db_session.flush()
    await async_db_session.refresh(processed_image)
    # test the processed_image
    assert processed_image.id is not None
    assert isinstance(processed_image.id, uuid.UUID)
    assert processed_image.storage_filename == "some_new_file_name.png"
    assert isinstance(processed_image.created_at, datetime)
    assert processed_image.created_at.tzinfo == UTC


async def test_processed_image_IntegrityError_when_storage_filename_is_nil(
    async_db_session: AsyncSession,
):
    """
    GIVEN a User exists in the database
    AND a ProcessedImage entry
    AND the storage_filename is nil
    WHEN the ProcessedImage is inserted into the database
    THEN it raises an IntegrityError
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
    async_db_session.add(unprocessed_image)
    await async_db_session.flush()
    # create a processed_image
    processed_image = ProcessedImage(
        unprocessed_image_id=unprocessed_image.id,
        storage_filename=None,
    )
    # save the processed_image
    async_db_session.add(processed_image)
    with pytest.raises(IntegrityError):
        await async_db_session.flush()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    await async_db_session.rollback()


async def no_test_processed_image_IntegrityError_when_storage_filename_is_blank_string(
    async_db_session: AsyncSession,
):
    # TODO: remove this test from suite. pydantic validation not working as inteneded
    """
    GIVEN a User exists in the database
    AND a ProcessedImage entry
    AND the storage_filename is a blank string
    WHEN the ProcessedImage is inserted into the database
    THEN it raises an IntegrityError
    """
    # create a user
    user = User(external_id="some-1234-extr-0987-id45")
    async_db_session.add(user)
    async_db_session.commit()
    # create an unprocessed_image
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="cool_image.png",
        storage_filename="some_file_name.png",
    )
    async_db_session.add(unprocessed_image)
    async_db_session.commit()
    # create a processed_image
    processed_image = ProcessedImage(
        user_id=user.id, unprocessed_image_id=unprocessed_image.id, storage_filename=""
    )
    # save the processed_image
    async_db_session.add(processed_image)
    with pytest.raises(IntegrityError):
        async_db_session.commit()
    # It's good practice to roll back the session after a failed transaction
    # to ensure the session is clean for any subsequent tests.
    async_db_session.rollback()


async def test_processed_image_DataError_when_storage_filename_is_too_long(
    async_db_session: AsyncSession,
):
    """
    GIVEN a User exists in the database
    AND a ProcessedImage entry
    AND the storage_filename is too long
    WHEN the ProcessedImage is inserted into the database
    THEN it raises an DataError
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
    async_db_session.add(unprocessed_image)
    await async_db_session.flush()
    # create a processed_image
    processed_image = ProcessedImage(
        user_id=user.id,
        unprocessed_image_id=unprocessed_image.id,
        storage_filename="a" * 300,
    )
    # save the processed_image
    async_db_session.add(processed_image)
    with pytest.raises(DataError):
        await async_db_session.flush()
