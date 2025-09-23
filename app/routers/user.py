import logging
from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlmodel import Session, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.schemas.transactions_db.user import User
from app.schemas.user import UserRead
from app.dependency.async_dependency import get_current_external_user_id
from app.services.user import create_user, get_user_by_external_id, delete_user, UserNotFound, PermissionDenied
import uuid

router = APIRouter()
# set up logging
logger = logging.getLogger(__name__)

@router.post(
    path="/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user_endpoint(
    *,
    db_session: AsyncSession = Depends(get_session),
    external_id: str = Depends(get_current_external_user_id)
):
    """
        Creates a new user in the database based on a trusted external ID.

        This endpoint is idempotent; if a user with the given external ID already
        exists, it will return a 409 Conflict error instead of creating a duplicate.

        params:
            *: Enforces that all subsequent parameters must be specified by keyword.
            db_session: The database session, injected by the `get_session` dependency.
            external_id: The user's external ID, injected by the security dependency.
    """
    # NOTE --->
    #   trust but verify
    #   the external_id comes from an external source of your choice.
    #   it is suggested that you verify the existence of the external_id before continuing.
    #   this is highly dependent on how you use this app.
    #   probably you should do that here where this comment is...
    # <--- NOTE
    # call the service to check for an existing user
    existing_user = get_user_by_external_id(
        db_session=db_session, external_id=external_id
    )
    # the endpoint handles the HTTP-specific logic
    if existing_user:
        # already have this user
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with external_id '{external_id}' already exists."
        )
    # call the service to create the new user
    new_user = create_user(db_session=db_session, external_id=external_id)
    # convert the SQLModel object to your Pydantic UserRead schema
    # this only works because UserRead has `from_attributes=True` and SQLModel is Pydantic-compatible.
    return UserRead.model_validate(new_user)

@router.post(
    path="/sign-in",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
def sign_in_user_endpoint(
    *,
    db_session: AsyncSession = Depends(get_session),
    external_id: str = Depends(get_current_external_user_id)
):
    """
        Finds a user based on their external ID and returns their details.

        This endpoint confirms that a user who has been authenticated by an
        external service also exists in this application's database.

        params:
           *: Enforces that all subsequent parameters must be specified by keyword.
            db_session: The database session, injected by the `get_session` dependency.
            external_id: The user's external ID, from the security dependency.
    """
    # Find the user in the database using their trusted external ID.
    user = get_user_by_external_id(
        db_session=db_session, external_id=external_id
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
    path="/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_endpoint(
    *,
    db_session: AsyncSession = Depends(get_session),
    external_id: str = Depends(get_current_external_user_id),
    user_id: Annotated[uuid.UUID, Path(title="The ID of the item to destroy")],
):
    """
        Deletes a user from the database.

        A user can only delete their own account. This is verified by ensuring
        the `external_id` from the authentication token matches the `external_id`
        of the user record being deleted.

        params:
           *: Enforces that all subsequent parameters must be specified by keyword.
            db_session: The database session, injected by the `get_session` dependency.
            external_id: The user's external ID, from the security dependency.
            user_id: The unique ID of the user to be deleted, from the URL path.
    """
    try:
        delete_user(
            db_session=db_session,
            user_id_to_delete=user_id,
            requesting_external_id=external_id,
        )
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionDenied as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    # according to HTTP standards, a successful DELETE should return 204 No Content.
    return None
