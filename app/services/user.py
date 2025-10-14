import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.exceptions as exc
import app.repository as repository_layer
from app.db.database import get_async_session
from app.dependency.async_dependency import get_current_external_user_id
from app.repository.directory_manager import (
    create_processed_user_directory,
    create_unprocessed_user_directory,
)
from app.schemas.transactions_db.user import User
from app.schemas.user import ResponseSignInUser, ResponseSignUpUser

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
    existing_user = await repository_layer.get_user_by_external_id(
        external_id=external_id,
        db_session=db_session
    )
    if existing_user:
        # already have this user
        raise exc.UserAlreadyExists(f"User with external id {external_id} already exists")
    # --- Create the User ---
    new_user = await repository_layer.create_user(
        external_id=external_id,
        db_session=db_session
    )
    # --- create some subdirectories to organize the image data ---
    await create_unprocessed_user_directory(
        user_id=new_user.id,
    )
    await create_processed_user_directory(
        user_id=new_user.id,
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
    user_record = await db_session.get(
        User,
        user_id_to_delete,
    )
    # --- Check If User Exists ---
    if not user_record:
        raise exc.UserNotFound(
            f"User with id '{user_id_to_delete}' not found."
        )
    # --- Check If Authorized ---
    if user_record.external_id != external_id:
        raise exc.PermissionDenied(
            "You do not have permission to delete this user."
        )
    # --- Delete The Entry ---
    await db_session.delete(user_record)
    await db_session.commit()
    return None

async def sign_in_user_service(
    external_id: str = Depends(get_current_external_user_id),
    db_session: AsyncSession = Depends(get_async_session)
) -> ResponseSignInUser | None:
    # --- Get the User ---
    entry = await repository_layer.get_user_by_external_id(
        external_id=external_id,
        db_session=db_session
    )
    # --- Check If User Exists ---
    if not entry:
        raise exc.UserNotFound(
            f"User with external id '{external_id}' not found."
        )
    return ResponseSignInUser(
        id=entry.id,
        external_id=external_id,
    )
