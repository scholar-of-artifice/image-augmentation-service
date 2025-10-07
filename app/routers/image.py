import uuid
from typing import Annotated

from fastapi import status, APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

import app.exceptions as exc
from app.db.database import get_async_session
from app.dependency.async_dependency import get_current_active_user
from app.internal.file_handling import VOLUME_PATHS
from app.schemas.image import ResponseUploadImage
from app.schemas.transactions_db.user import User
from app.services.image import (
    get_processed_image_by_id,
    get_unprocessed_image_by_id,
    save_unprocessed_image,
    upload_image_service,
)
from app.dependency.async_dependency import get_current_external_user_id
from app.repository.directory_manager import write_unprocessed_image
from app.services.user import sign_in_user_service

router = APIRouter()

@router.post(
    path="/upload",
    response_model=ResponseUploadImage,
    status_code=status.HTTP_201_CREATED
)
async def upload_image_endpoint(
        image: Annotated[
            UploadFile,
            File(
                description="The image file to upload"
            )
        ],
        current_user: User = Depends(get_current_active_user),
        db_session: AsyncSession = Depends(get_async_session),
) -> ResponseUploadImage:
    try:
        return await upload_image_service(
            image_file=image,
            user_id=current_user.id,
            db_session=db_session,
        )
    except exc.UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e

# #@router.post(
# #    path="/upload/",
# #    response_model=ResponseUploadImage
# #)
# #async def upload_endpoint(
# #        file: Annotated[
# #            UploadFile,
# #            File(
# #                description="The image file to upload."
# #            )
# #        ],
# #        db_session: AsyncSession = Depends(get_async_session),
# #        current_user: User = Depends(get_current_active_user)
# #):
# #    """
# #    # Description
# #    Use this endpoint to upload an image for later processing.
# #
# #    ## User Story
# #
# #    ```
# #    As a user ...
# #    I want to store an image ...
# #    so that I can make augmented versions in the future.
# #    ```
# #
# #    ### Internal Details
# #    - **db_session**: Injected database session for database operations.
# #    - **current_user**: The user who wants to upload the image.
# #    """
# #    return await save_unprocessed_image(
# #        file=file,
# #        db_session=db_session,
# #        user_id=current_user.id
# #    )
# #
# #@router.get(
# #    path="/unprocessed-image/{unprocessed_image_id}/",
# #    response_class=FileResponse
# #)
# #async def get_unprocessed_image_by_id_endpoint(
# #        unprocessed_image_id: uuid.UUID,
# #        db_session: AsyncSession = Depends(get_async_session),
# #        current_user: User = Depends(get_current_active_user)
# #):
# #    """
# #        Get an unprocessed image by its ID.
# #
# #        Arguments:
# #            unprocessed_image_id {str} -- The id of the unprocessed image.
# #    """
# #    # get the image
# #    image_entry = await get_unprocessed_image_by_id(
# #        unprocessed_image_id=unprocessed_image_id,
# #        db_session=db_session,
# #        user_id=current_user.id
# #    )
# #    # if nothing is found an error should be raised by the service
# #    # if an image entry is found
# #    if image_entry:
# #        image_path = VOLUME_PATHS["unprocessed_image_data"] / image_entry.storage_filename
# #
# #        return FileResponse(
# #            path=image_path.with_suffix('.png'),
# #            media_type="image/png",
# #            filename=str(image_entry.storage_filename) + '.png',
# #        )
# #    return None
# #
# #
# #@router.get(
# #    path="/processed-image/{processed_image_id}/",
# #    response_class=FileResponse
# #)
# #async def get_processed_image_by_id_endpoint(
# #        processed_image_id: uuid.UUID,
# #        db_session: AsyncSession = Depends(get_async_session),
# #        current_user: User = Depends(get_current_active_user)
# #):
# #    """
# #        Get a processed image by its ID.
# #
# #        Arguments:
# #            processed_image_id {str} -- The id of the unprocessed image.
# #    """
# #    # get the image
# #    image_entry = await get_processed_image_by_id(
# #        processed_image_id=processed_image_id,
# #        db_session=db_session,
# #        user_id=current_user.id
# #    )
# #    # if nothing is found an error should be raised by the service
# #    # if an image entry is found
# #    if image_entry:
# #        image_path = VOLUME_PATHS["processed_image_data"] / image_entry.storage_filename
# #
# #        return FileResponse(
# #            path=image_path.with_suffix('.png'),
# #            media_type="image/png",
# #            filename=str(image_entry.storage_filename) + '.png',
# #        )
# #    return None
# #
# #
# #