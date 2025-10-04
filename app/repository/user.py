from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.database import get_async_session
from app.schemas.transactions_db.user import User


async def create_user(
    external_id: str,
    db_session: AsyncSession = Depends(get_async_session)
) -> User:
    """
    - create a new user in the transaction database
    - returns the newly created User object.
    """
    user_record = User(external_id=external_id)
    db_session.add(user_record)
    await db_session.flush()
    await db_session.refresh(user_record)
    await db_session.commit()
    return user_record

async def get_user_by_external_id(
    external_id: str,
    db_session: AsyncSession = Depends(get_async_session)
) -> User | None:
    """
    Retrieves a user from the database by their external ID.
    Returns the User object or None if not found.
    This function should not raise an exception.or HTTPError.
    """
    result = await db_session.execute(
        select(User).where(
            User.external_id == external_id
        )
    )
    user_record = result.scalars().first()
    # --- return relevant information to user ---
    return user_record

