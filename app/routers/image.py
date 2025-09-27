from pathlib import Path
from app.internal.file_handling import VOLUME_PATHS
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.dependency.async_dependency import get_body_as_model, get_current_active_user
from app.schemas.image import ImageProcessResponse, UploadRequestBody
from app.schemas.transactions_db.user import User
from app.services.image import process_and_save_image, get_unprocessed_image_by_id
import uuid
router = APIRouter()


@router.post(
    path="/upload/",
    response_model=ImageProcessResponse
)
async def upload_endpoint(
        file: UploadFile,
        validated_data: UploadRequestBody = Depends(get_body_as_model),
        db_session: AsyncSession = Depends(get_async_session),
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

@router.get(
    path="unprocessed-image/{unprocessed_image_id}/",
    response_class=FileResponse
)
async def get_unprocessed_image_by_id_endpoint(
        unprocessed_image_id: uuid.UUID,
        db_session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_active_user)
):
    """
        Get an unprocessed image by its ID.

        Arguments:
            unprocessed_image_id {str} -- The id of the unprocessed image.
    """
    image = await get_unprocessed_image_by_id(
        unprocessed_image_id=unprocessed_image_id,
        db_session=db_session,
        user_id=current_user.id
    )
    image_path = VOLUME_PATHS["unprocessed_image_data"] / image.storage_filename

    return FileResponse(
        path=image_path,
        media_type=image.media_type,
        filename=image.storage_filename,
    )


