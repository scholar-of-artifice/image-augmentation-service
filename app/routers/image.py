from pathlib import Path
from app.internal.file_handling import VOLUME_PATHS
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.database import get_async_session
from app.dependency.async_dependency import get_body_as_model, get_current_active_user
from app.schemas.image import ResponseUploadImage, ResponseAugmentImage, AugmentRequestBody
from app.schemas.transactions_db.user import User
from app.services.image import process_and_save_image, upload_service, get_unprocessed_image_by_id, get_processed_image_by_id
import uuid
router = APIRouter()


@router.post(
    path="/upload/",
    response_model=ResponseUploadImage
)
async def upload_endpoint(
        file: Annotated[
            UploadFile,
            File(
                description="The image file to upload."
            )
        ],
        db_session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_active_user)
):
    """
    # Description
    Use this endpoint to upload an image for later processing.

    ## User Story

    ```
    As a user ...
    I want to store an image ...
    so that I can make augmented versions in the future.
    ```

    ### Internal Details
    - **db_session**: Injected database session for database operations.
    - **current_user**: The user who wants to upload the image.
    """
    return await upload_service(
        file=file,
        db_session=db_session,
        user_id=current_user.id
    )

@router.post(
    path="/augment/",
    response_model=ResponseAugmentImage
)
async def augment_endpoint(
    augment_request: AugmentRequestBody,
    db_session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    # Description
    Use this endpoint to augment an image.

    ## User Story
    ```
    As a user ...
    I want to augment an image ...
    and receive information about where to find that image...
    so that I can use my augmented data in the future.
    ```

    ### Internal Details
    - **db_session**: Injected database session for database operations.
    - **current_user**: The user who wants to upload the image.
    """
    # TODO: get the image from block storage
    # TODO: make an augmented image
    # TODO: persist augmented image to block storage
    # TODO: put an entry in the database for the augmented image
    return ResponseAugmentImage(
        unprocessed_image_id=uuid.uuid4(),
        processed_image_id=uuid.uuid4(),
        processed_image_filename='cool filename bro',
        request_body=augment_request,
    )

@router.get(
    path="/unprocessed-image/{unprocessed_image_id}/",
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
    # get the image
    image_entry = await get_unprocessed_image_by_id(
        unprocessed_image_id=unprocessed_image_id,
        db_session=db_session,
        user_id=current_user.id
    )
    # if nothing is found an error should be raised by the service
    # if an image entry is found
    if image_entry:
        image_path = VOLUME_PATHS["unprocessed_image_data"] / image_entry.storage_filename
    
        return FileResponse(
            path=image_path.with_suffix('.png'),
            media_type="image/png",
            filename=str(image_entry.storage_filename) + '.png',
        )
    return None


@router.get(
    path="/processed-image/{processed_image_id}/",
    response_class=FileResponse
)
async def get_processed_image_by_id_endpoint(
        processed_image_id: uuid.UUID,
        db_session: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(get_current_active_user)
):
    """
        Get a processed image by its ID.

        Arguments:
            processed_image_id {str} -- The id of the unprocessed image.
    """
    # get the image
    image_entry = await get_processed_image_by_id(
        processed_image_id=processed_image_id,
        db_session=db_session,
        user_id=current_user.id
    )
    # if nothing is found an error should be raised by the service
    # if an image entry is found
    if image_entry:
        image_path = VOLUME_PATHS["processed_image_data"] / image_entry.storage_filename

        return FileResponse(
            path=image_path.with_suffix('.png'),
            media_type="image/png",
            filename=str(image_entry.storage_filename) + '.png',
        )
    return None


