import uuid
from collections.abc import Callable

import sqlalchemy
from fastapi import Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse
from app.db.database import get_async_session
from app.internal.augmentations import rainbow_noise, rotate, shift
from app.internal.file_handling import (
    create_file_name,
    translate_file_to_numpy_array,
    write_numpy_array_to_image_file,
)
from app.repository import (
    create_processed_image_directory,
    create_UnprocessedImage_entry,
    create_ProcessedImage_entry,
    process_image,
    read_unprocessed_image_from_disc,
    read_UnprocessedImage_entry,
    read_ProcessedImage_entry,
    write_processed_image_to_disc,
    write_unprocessed_image_to_disc,
    does_unprocessed_image_file_exist,
    get_unprocessed_image_location,
    does_processed_image_file_exist,
    get_processed_image_location
)
from app.schemas.image import (
    AugmentationRequestBody,
    ResponseAugmentImage,
    ResponseUploadImage,
    UploadRequestBody,
)
from app.schemas.transactions_db import (
    ProcessedImage,
    UnprocessedImage,
    User,
)


async def upload_image_service(
        image_file: UploadFile,
        user_id: uuid.UUID,
        db_session: AsyncSession = Depends(get_async_session),
) -> ResponseUploadImage:
    """
    Upload a new unprocessed image.
    Creates an entry in the database.
    Creates a file in the block storage to be retrieved later.
    """
    # TODO: any other raised exceptions and such...
    # asynchronously read the contents of the uploaded file as bytes
    image_content = await image_file.read()
    # create a filename
    filename = f"{uuid.uuid4()}.png"
    # persist image to storage volume
    file_path = await write_unprocessed_image_to_disc(
        image_content=image_content,
        user_id=user_id,
        storage_filename=filename
    )
    print(f"Uploaded {filename} to {file_path}")
    # persist entry to transactions database
    data_entry = await create_UnprocessedImage_entry(
        original_filename=image_file.filename,
        storage_filename=filename,
        user_id=user_id,
        db_session=db_session,
    )
    unprocessed_image_id = data_entry.id
    # create the processed image subdirectory
    await create_processed_image_directory(
        user_id=user_id,
        image_id=unprocessed_image_id
    )
    # return relevant information
    return ResponseUploadImage(
        unprocessed_image_id=unprocessed_image_id,
        unprocessed_image_filename=filename,
    )

async def augment_image_service(
        unprocessed_image_id: uuid.UUID,
        processing_request: AugmentationRequestBody,
        user_id: uuid.UUID,
        db_session: AsyncSession = Depends(get_async_session),
) -> ResponseAugmentImage:
    # read the UnprocessedImage from the database
    unprocessed_image_entry = await read_UnprocessedImage_entry(
        image_id=unprocessed_image_id,
        user_id=user_id,
        db_session=db_session,
    )
    # get the unprocessed_image from block storage
    unprocessed_image_data = await read_unprocessed_image_from_disc(
        user_id=user_id,
        storage_filename=unprocessed_image_entry.storage_filename,
    )
    # make an augmentation
    processed_image_data = await process_image(
        image_data=unprocessed_image_data,
        processing_parameters=processing_request
    )
    # make a filename
    storage_filename = f"{uuid.uuid4()}.png"
    # persist the image to block storage
    stored_at = await write_processed_image_to_disc(
        image_data=processed_image_data,
        user_id=user_id,
        unprocessed_image_id=unprocessed_image_id,
        storage_filename=storage_filename
    )
    print(f"Uploaded {storage_filename} to {stored_at}")
    # make an entry in the database

    # return the important information
    return ResponseAugmentImage(
        unprocessed_image_id=unprocessed_image_id,
        processed_image_id=uuid.uuid4(),
        processed_image_filename=storage_filename,
        request_body=processing_request
    )

async def get_unprocessed_image_by_id_service(
        unprocessed_image_id: uuid.UUID,
        user_id: uuid.UUID,
        db_session: AsyncSession = Depends(get_async_session),
) -> FileResponse:
    # get the UnprocessedImage entry from the database
    image_entry = await get_unprocessed_image_entry_by_id(
        unprocessed_image_id=unprocessed_image_id,
        user_id=user_id,
        db_session=db_session,
    )
    # check if the entry exists
    if not image_entry:
        # TODO: raise error
        return None
    # check if the file exists
    # TODO: this can be improved
    if await does_unprocessed_image_file_exist(
        user_id=user_id,
        unprocessed_image_storage_filename=image_entry.storage_filename,
    ):
        image_path = await get_unprocessed_image_location(
            user_id=user_id,
            unprocessed_image_storage_filename=image_entry.storage_filename,
        )
        # it exists
        return FileResponse(
            path=image_path.with_suffix('.png'),
            media_type="image/png",
            filename=str(image_entry.storage_filename) + '.png',
        )
    else:
        # it does not exist
        # TODO: raise error
        return None

async def get_processed_image_by_id_service(
        processed_image_id: uuid.UUID,
        user_id: uuid.UUID,
        db_session: AsyncSession = Depends(get_async_session),
) -> FileResponse:
    # get the ProcessedImage entry from the database
    image_entry = await get_processed_image_entry_by_id(
        unprocessed_image_id=processed_image_id,
        user_id=user_id,
        db_session=db_session,
    )
    # check if the entry exists
    if not image_entry:
        # TODO: raise error
        return None
    # check if the file exists
    # TODO: this can be improved
    if await does_processed_image_file_exist(
        user_id=user_id,
        processed_image_storage_filename=image_entry.storage_filename,
    ):
        image_path = await get_processed_image_location(
            user_id=user_id,
            processed_image_storage_filename=image_entry.storage_filename,
        )
        # it exists
        return FileResponse(
            path=image_path.with_suffix('.png'),
            media_type="image/png",
            filename=str(image_entry.storage_filename) + '.png',
        )
    else:
        # it does not exist
        # TODO: raise error
        return None

