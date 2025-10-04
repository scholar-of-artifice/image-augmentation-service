import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.database import get_async_session
from app.dependency.async_dependency import get_current_external_user_id
from app.schemas.transactions_db.user import User
from app.schemas.user import ResponseSignUpUser, ResponseSignInUser

# --- Custom Exceptions ---
# TODO: might move these later
class UserNotFound(Exception):
    """
    Raised when a user is not found in the database.
    """

    pass


class UserAlreadyExists(Exception):
    """
    Raised when a user is already in the database.
    """

    pass


class PermissionDenied(Exception):
    """
    Raised when a user is not authorized to perform an action.
    """

    pass

# --- these are the functions that the endpoint calls ---

async def sign_up_user_service(
    external_id: str = Depends(get_current_external_user_id),
    db_session: AsyncSession = Depends(get_async_session)
) -> ResponseSignUpUser:
    # NOTE --->
    #   trust but verify
    #   the external_id comes from an external source of your choice.
    #   it is suggested that you verify the existence of the external_id before continuing.
    #   this is highly dependent on how you use this app.
    #   probably you should do that here where this comment is...
    # <--- NOTE
    # --- Check if User exists ---
    existing_user = await get_user_by_external_id(
        db_session=db_session,
        external_id=external_id
    )
    if existing_user:
        # already have this user
        raise UserNotFound(f"User with external id {external_id} already exists")
    # --- Create the User ---
    new_user = await create_user(
        db_session=db_session,
        external_id=external_id
    )
    # --- return relevant information to user ---
    return ResponseSignUpUser(
        id=new_user.id,
        external_id=external_id,
    )

async def delete_user_service(
    user_id_to_delete: uuid.UUID,
    external_id: str = Depends(get_current_external_user_id),
    db_session: AsyncSession = Depends(get_async_session)
) -> None:
    """
    Deletes a user after verifying the requesting user has permission.
    Raises UserNotFound or PermissionDenied on failure.
    """
    # --- Get The User To Delete ---
    user_to_delete = await db_session.get(
        User,
        user_id_to_delete
    )
    # --- Check If User Exists ---
    if not user_to_delete:
        raise UserNotFound(
            f"User with id '{user_id_to_delete}' not found."
        )
    # --- Check If Authorized ---
    if user_to_delete.external_id != external_id:
        raise PermissionDenied(
            "You do not have permission to delete this user."
        )
    # --- Delete The Entry ---
    await db_session.delete(user_to_delete)
    await db_session.commit()
    return None

# --- these are the important utility functions that are used ---
# TODO: probably move these

async def create_user(
        db_session: AsyncSession,
        external_id: str
) -> User:
    """
    - create a new user in the transaction database
    - returns the newly created User object.
    """
    db_user = User(external_id=external_id)
    db_session.add(db_user)
    await db_session.flush()
    await db_session.refresh(db_user)
    await db_session.commit()
    return db_user

async def get_user_by_external_id(
        external_id: str,
        db_session: AsyncSession,
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
    return ResponseSignInUser(
        id=user_record.id,
        external_id=external_id,
    )

