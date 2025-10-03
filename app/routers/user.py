import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.dependency.async_dependency import get_current_external_user_id
from app.schemas.user import ResponseCreateUser, UserRead
from app.services.user import (
    PermissionDenied,
    UserNotFound,
    delete_user,
    get_user_by_external_id,
    sign_up_service,
)

router = APIRouter()
# set up logging
logger = logging.getLogger(__name__)

@router.post(
    path="/sign-up/",
    response_model=ResponseCreateUser,
    status_code=status.HTTP_201_CREATED,
)
async def sign_up_user_endpoint(
    db_session: AsyncSession = Depends(get_async_session),
    external_id: str = Depends(get_current_external_user_id)
):
    """
        Creates a new user in the database based on a trusted external ID.

        This endpoint is idempotent; if a user with the given external ID already
        exists, it will return a 409 Conflict error instead of creating a duplicate.

        params:
            *: Enforces that all subsequent parameters must be specified by keyword.
            db_session: The database session, injected by the `get_async_session` dependency.
            external_id: The user's external ID, injected by the security dependency.
    """
    # NOTE --->
    #   trust but verify
    #   the external_id comes from an external source of your choice.
    #   it is suggested that you verify the existence of the external_id before continuing.
    #   this is highly dependent on how you use this app.
    #   probably you should do that here where this comment is...
    # <--- NOTE
    return await sign_up_service(
        db_session=db_session,
        external_id=external_id
    )

@router.post(
    path="/sign-in",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def sign_in_user_endpoint(
    *,
    db_session: AsyncSession = Depends(get_async_session),
    external_id: str = Depends(get_current_external_user_id)
):
    """
        Finds a user based on their external ID and returns their details.

        This endpoint confirms that a user who has been authenticated by an
        external service also exists in this application's database.

        params:
           *: Enforces that all subsequent parameters must be specified by keyword.
            db_session: The database session, injected by the `get_async_session` dependency.
            external_id: The user's external ID, from the security dependency.
    """
    # Find the user in the database using their trusted external ID.
    user = await get_user_by_external_id(
        db_session=db_session,
        external_id=external_id
    )
    # If no user is found, they exist externally but not in our system.
    # The client should call the POST /users endpoint to create them.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please create an account first."
        )
    # If the user is found and active, return their data.
    return UserRead.model_validate(user)

@router.delete(
    path="/user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_endpoint(
    user_id: Annotated[uuid.UUID, Path(title="The ID of the item to destroy")],
    db_session: AsyncSession = Depends(get_async_session),
    external_id: str = Depends(get_current_external_user_id),
):
    """
        Deletes a user from the database.

        A user can only delete their own account. This is verified by ensuring
        the `external_id` from the authentication token matches the `external_id`
        of the user record being deleted.

        params:
           *: Enforces that all subsequent parameters must be specified by keyword.
            db_session: The database session, injected by the `get_async_session` dependency.
            external_id: The user's external ID, from the security dependency.
            user_id: The unique ID of the user to be deleted, from the URL path.
    """
    try:
        await delete_user(
            db_session=db_session,
            user_id_to_delete=user_id,
            requesting_external_id=external_id,
        )
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except PermissionDenied as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        ) from e
    # according to HTTP standards, a successful DELETE should return 204 No Content.
    return None
