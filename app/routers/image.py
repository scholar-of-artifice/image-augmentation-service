from fastapi import (APIRouter, Depends, UploadFile)
from app.dependency.async_dependency import get_current_active_user
from app.schemas.image import UploadRequestBody, ImageProcessResponse
from app.dependency.async_dependency import get_body_as_model
from app.services.image import process_and_save_image
from app.db.database import get_session
from app.schemas.transactions_db.user import User
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    path="/upload/",
    response_model=ImageProcessResponse
)
async def upload_endpoint(
        file: UploadFile,
        validated_data: UploadRequestBody = Depends(get_body_as_model),
        db_session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_active_user)
):
    """
        Request processing of an image file.

        Arguments:
            file {UploadFile} -- The image file to be processed.
            validated_data {UploadRequestBody} -- The parsed and validated request body.
    """
    return await process_and_save_image(
        file=file,
        validated_data=validated_data,
        db_session=db_session,
        user_id=current_user.id
    )

