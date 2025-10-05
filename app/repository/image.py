import uuid

from app.schemas.transactions_db import UnprocessedImage
from app.exceptions import ImageNotFound, PermissionDenied
from fastapi import Depends
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session

async def store_unprocessed_image(
) -> None:
    return None


async def create_UnprocessedImage_entry(
    original_filename: str,
    storage_filename: str,
    user_id: uuid.UUID,
    db_session: AsyncSession = Depends(get_async_session)
) -> UnprocessedImage:
    """
    Create an unprocessed image entry.
    Write unprocessed image entry to database.
    """
    # create the UnprocessedImage entry
    new_entry = UnprocessedImage(
        original_filename=original_filename,
        storage_filename=storage_filename,
        user_id=user_id,
    )
    # attempt to write it to the Transactions Database
    db_session.add(new_entry)
    await db_session.flush()
    await db_session.refresh(new_entry)
    await db_session.commit()
    # return the entry
    return new_entry


async def read_UnprocessedImage_entry(
    image_id: uuid.UUID,
    user_id: uuid.UUID,
    db_session: AsyncSession = Depends(get_async_session)
) -> UnprocessedImage:
    """
    Find an UnprocessedImage entry.
    Return the UnprocessedImage entry if it exists.
    """
    # make the query
    query = sqlalchemy.select(UnprocessedImage).where(
            UnprocessedImage.id == image_id
        ).where(
            UnprocessedImage.user_id == user_id
        )
    # execute the query
    result = await db_session.execute(query)
    # evaluate if entry exists
    entry = result.scalar_one_or_none()
    if entry is None:
        raise ImageNotFound(
            f'Image with id {image_id} not found',
        )
    # return the entry
    return entry