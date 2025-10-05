import uuid

from app.schemas.transactions_db import UnprocessedImage
from app.exceptions import ImageNotFound, PermissionDenied
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session

async def store_unprocessed_image(
) -> None:
    return None


async def create_unprocessed_image_entry(
    original_filename: str,
    storage_filename: str,
    user_id: uuid.UUID,
    db_session: AsyncSession = Depends(get_async_session)
) -> UnprocessedImage:
    new_entry = UnprocessedImage(
        original_filename=original_filename,
        storage_filename=storage_filename,
        user_id=user_id,
    )
    db_session.add(new_entry)
    await db_session.flush()
    await db_session.refresh(new_entry)
    await db_session.commit()
    return new_entry


async def read_unprocessed_image_entry(
    id: uuid.UUID,
    user_id: uuid.UUID,
    db_session: AsyncSession = Depends(get_async_session)
) -> UnprocessedImage:
    entry_query = await db_session.query(UnprocessedImage).filter(
        UnprocessedImage.id == id,
    )
    entry = entry_query.first()
    if entry is None:
        raise ImageNotFound(
            f'Image with id {id} not found',
        )
    if entry.user_id != user_id:
        raise PermissionDenied(
            f'You do not have permission to access this image',
        )
    return entry