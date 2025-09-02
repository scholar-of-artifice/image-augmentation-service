from fastapi import Header, HTTPException, status
from typing import Annotated

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