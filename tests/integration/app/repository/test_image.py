import uuid
from datetime import datetime

import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.image import create_UnprocessedImage_entry, read_UnprocessedImage_entry
from app.schemas.transactions_db import UnprocessedImage, User

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def test_user(
        async_db_session: AsyncSession
) -> User:
    new_user = User(
        external_id=str(uuid.uuid4()),
    )
    async_db_session.add(new_user)
    await async_db_session.commit()
    await async_db_session.refresh(new_user)
    return new_user

async def test_create_UnprocessedImage_entry_success(
        async_db_session: AsyncSession,
        test_user: User,
):
    # create fake test data
    test_original_filename = 'my_cool_image.png'
    test_storage_filename = f"{uuid.uuid4()}.png"
    fake_user = await test_user
    test_user_id = fake_user.id
    # call the function
    new_entry = await create_UnprocessedImage_entry(
        original_filename=test_original_filename,
        storage_filename=test_storage_filename,
        user_id=test_user_id,
        db_session=async_db_session,
    )
    # check the results
    assert isinstance(new_entry, UnprocessedImage)
    assert new_entry.id is not None
    assert new_entry.original_filename == test_original_filename
    assert new_entry.storage_filename == test_storage_filename
    assert new_entry.user_id == test_user_id
    assert isinstance(new_entry.created_at, datetime)
    # verify it is in the database
    query = sqlalchemy.select(UnprocessedImage).where(UnprocessedImage.id == new_entry.id)
    result = await async_db_session.execute(query)
    db_entry = result.scalar_one_or_none()
    assert db_entry is not None
    assert db_entry.original_filename == test_original_filename
    assert db_entry.user_id == test_user_id


async def test_read_UnprocessedImage_entry_success(
        async_db_session: AsyncSession,
        test_user: User,
):
    # create fake test data
    test_original_filename = 'my_cool_image.png'
    test_storage_filename = f"{uuid.uuid4()}.png"
    fake_user = await test_user
    test_user_id = fake_user.id
    # create an UnprocessedImage
    new_image_entry = await create_UnprocessedImage_entry(
        original_filename=test_original_filename,
        storage_filename=test_storage_filename,
        user_id=test_user_id,
        db_session=async_db_session,
    )
    # call the function
    read_entry = await read_UnprocessedImage_entry(
        image_id=new_image_entry.id,
        user_id=test_user_id,
        db_session=async_db_session,
    )
    # check the results
    assert isinstance(read_entry, UnprocessedImage)
    assert read_entry == new_image_entry
