from fastapi import Header, HTTPException, status, Form
from typing import Annotated
from app.models.image_api.upload import UploadRequestBody
from pydantic import ValidationError
import json

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
