from typing import Annotated

from fastapi import Depends, Form, Header, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.db.database import get_async_session
from app.schemas.image import UploadRequestBody
from app.schemas.transactions_db.user import User


async def get_current_external_user_id(
    # Look for a header named "X-External-User-ID" in the request.
    # 'Annotated' is the modern way to add metadata like 'Header'.
    external_id: Annotated[str | None, Header(alias="X-External-User-ID")] = None
) -> str:
    """
        A dependency that simulates extracting a user's external ID from a request header.
    """
    # If the header is None or blank, raise an error.
    if not external_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-External-User-ID header"
        )
    # If the header is found, return its value.
    return external_id

async def get_body_as_model( body: str = Form() ) -> UploadRequestBody:
    """
        Looks at incoming JSON string and validates it against the UploadRequestBody schema.
        If the arguments are acceptable, it will return the UploadRequestBody.
    """
    try:
        # validate the incoming data against the pydantic model.
        return UploadRequestBody.model_validate_json(json_data=body)
    except ValidationError as e:
        # this should happen when any validation fails
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )

async def get_current_active_user(
        *,
        external_id: str = Depends(get_current_external_user_id),
        db_session: AsyncSession = Depends(get_async_session)
) -> User:
    """
        Gets the external_id from the token...
        finds the user in the database...
        and returns the complete User model object.
    """
    result = await db_session.execute(
        select(User).where(
            User.external_id == external_id
        )
    )
    user = result.scalars().first()
    if not user:
        # this protects against cases where a valid token is presented...
        # ... for a user who has since been deleted from our database.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user