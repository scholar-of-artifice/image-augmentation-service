import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.internal.database import get_session
from app.models.transactions_db.user import User
from app.models.user_api.create import UserRead
from app.dependency import get_current_external_user_id

router = APIRouter()
# set up logging
logger = logging.getLogger(__name__)

@router.post(
    path="/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    *,
    session: Session = Depends(get_session),
    external_id: str = Depends(get_current_external_user_id)
):
    """
        Creates a new user in the database based on a trusted external ID.

        This endpoint is idempotent; if a user with the given external ID already
        exists, it will return a 409 Conflict error instead of creating a duplicate.

        params:
            *: Enforces that all subsequent parameters must be specified by keyword.
            session: The database session, injected by the `get_session` dependency.
            external_id: The user's external ID, injected by the security dependency.
    """
    # NOTE --->
    #   trust but verify
    #   the external_id comes from an external source of your choice.
    #   it is suggested that you verify the existence of the external_id before continuing.
    #   this is highly dependent on how you use this app.
    #   probably you should do that here where this comment is...
    # <--- NOTE
    # query the database using SQLModel's syntax
    existing_user = session.exec(select(User).where(User.external_id == external_id)).first()
    # check for the user
    if existing_user:
        # already have this user
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with external_id '{external_id}' already exists."
        )
    # create an instance of the SQLModel User
    db_user = User(external_id=external_id)
    # add the user to the database
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    # convert the SQLModel object to your Pydantic UserRead schema
    # this only works because UserRead has `from_attributes=True` and SQLModel is Pydantic-compatible.
    return UserRead.model_validate(db_user)
