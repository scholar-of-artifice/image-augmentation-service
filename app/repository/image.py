import uuid

from app.schemas.transactions_db import UnprocessedImage
from app.exceptions import ImageNotFound, PermissionDenied
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session

async def store_unprocessed_image(
) -> None:
    return None
