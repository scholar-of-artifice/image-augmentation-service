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
    process_image,
    read_unprocessed_image_from_disc,
    read_UnprocessedImage_entry,
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
    # persist the image to block storage
    storage_filename = f"{uuid.uuid4()}.png"
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


async def save_unprocessed_image(
        file: UploadFile,
        user_id: uuid.UUID,
        db_session: AsyncSession,
        # --- INJECTED DEPENDENCIES ---
        file_translator: Callable = translate_file_to_numpy_array,
        file_writer: Callable = write_numpy_array_to_image_file,
        filename_creator: Callable = create_file_name,
) -> ResponseUploadImage:
    """
    Saves and UnprocessedImage to block storage and...
    creates a corresponding entry to the transactions database.
    """
    # --- Check Input Data ---
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided."
        )
    # read and convert the image
    # asynchronously read the contents of the uploaded file as bytes
    image_content = await file.read()
    # create a new filename
    unprocessed_storage_filename = filename_creator()
    # --- Save Relevant Unprocessed Image Data ---
    unprocessed_image_record = UnprocessedImage(
        original_filename=file.filename,  # use the original name from the file
        storage_filename=unprocessed_storage_filename,  # use a unique name
        user_id=user_id,  # associate to the user_id
    )
    # --- Persist Image to Storage ---
    # save a copy of the original unprocessed image to the 'unprocessed_image_data' volume.
    unprocessed_image_location = file_writer(
        data=image_content,
        file_name=unprocessed_storage_filename,
        destination_volume="unprocessed_image_data",
    )
    # --- Persist Record to Database ---
    # persist the data
    db_session.add(
        unprocessed_image_record
    )
    await db_session.flush()
    await db_session.refresh(unprocessed_image_record)
    await db_session.commit()
    # --- Formulate a Response ---
    # give the user what they need to query for the data
    return ResponseUploadImage(
        unprocessed_image_id=unprocessed_image_record.id,
        unprocessed_image_filename=unprocessed_image_record.storage_filename,
    )


async def process_and_save_image(
    file: UploadFile,
    validated_data: UploadRequestBody,
    db_session: AsyncSession,
    user_id: uuid.UUID,
    # --- INJECTED DEPENDENCIES ---
    file_translator: Callable = translate_file_to_numpy_array,
    file_writer: Callable = write_numpy_array_to_image_file,
    filename_creator: Callable = create_file_name,
    shift_processor: Callable = shift,  # TODO: this is probably changing later
    rotate_processor: Callable = rotate,  # TODO: this is probably changing later
    rainbow_noise_processor: Callable = rainbow_noise,  # TODO: this is probably changing later
) -> None:
    """
    Handles the core logic of processing and saving an image.
    """
    # read and convert the image
    # asynchronously read the contents of the uploaded file as bytes
    image_content = await file.read()
    # convert the raw image bytes into a numpy array
    image_data = file_translator(image_content)
    # --- Save Relevant Unprocessed Image Data ---
    unprocessed_storage_filename = filename_creator()
    unprocessed_image_record = UnprocessedImage(
        original_filename=file.filename,  # use the original name from the file
        storage_filename=unprocessed_storage_filename,  # use a unique name
        user_id=user_id,  # associate to the user_id
    )
    # save a copy of the original unprocessed image to the 'unprocessed_image_data' volume.
    unprocessed_image_location = file_writer(
        data=image_data,
        file_name=unprocessed_storage_filename,
        destination_volume="unprocessed_image_data",
    )
    # --- Process the Image ---
    # initialize a new variables for the processed image data
    new_img_data = image_data
    # check the processing argument from the request to determine which action to take
    if validated_data.arguments.processing == "shift":
        # apply shift
        new_img_data = shift_processor(
            image_data=image_data,
            direction=validated_data.arguments.direction,
            distance=validated_data.arguments.distance,
        )
    elif validated_data.arguments.processing == "rotate":
        # apply rotate
        new_img_data = rotate_processor(
            image_data=image_data, angle=validated_data.arguments.angle
        )
    elif validated_data.arguments.processing == "rainbow_noise":
        # apply rainbow_noise
        new_img_data = rainbow_noise_processor(
            image_data=image_data, amount=validated_data.arguments.amount
        )
    # --- Save Relevant Processed Image Data ---
    processed_storage_filename = filename_creator()
    processed_image_record = ProcessedImage(
        storage_filename=processed_storage_filename,  # use a unique name
    )
    # save the processed image to the 'processed_image_data' volume.
    processed_image_location = file_writer(
        data=new_img_data,
        file_name=processed_storage_filename,
        destination_volume="processed_image_data",
    )
    # --- Link the Records ---
    # link the processed image back to its unprocessed parent.
    unprocessed_image_record.processed_images.append(processed_image_record)
    # --- Persist to Database ---
    # persist the data
    db_session.add(
        unprocessed_image_record
    )  # only need to add the parent; SQLAlchemy handles the rest
    await db_session.flush()
    await db_session.refresh(unprocessed_image_record)
    await db_session.refresh(processed_image_record)
    await db_session.commit()
    # return an ImageProcessResponse
    # eturn ImageProcessResponse(
    #    unprocessed_image_id=unprocessed_image_record.id,
    #    unprocessed_image_filename=str(unprocessed_image_record.storage_filename) + ".png",
    #    processed_image_id=processed_image_record.id,
    #    processed_image_filename=str(processed_image_record.storage_filename) + ".png",
    #    processing_job_id=uuid.uuid4(), # TODO... fix this later when using worker
    #    body=validated_data,
    #
    return None


async def get_unprocessed_image_entry_by_id(
    unprocessed_image_id: uuid.UUID,
    db_session: AsyncSession,
    user_id: uuid.UUID
) -> UnprocessedImage:
    """
    Retrieves an unprocessed image by its ID.
    """
    # go find the user with this id
    query_for_user = sqlalchemy.select(User).where(
        User.id == user_id
    )
    response_for_user = await db_session.execute(query_for_user)
    user_entry = response_for_user.scalar_one_or_none()
    # raise an exception if no user exists
    if not user_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found with ID {user_id}",
        )
    # go find the UnprocessedImage where the user_id matches and the image_id matches
    query_for_image = sqlalchemy.select(UnprocessedImage).where(
        UnprocessedImage.user_id == user_entry.id,
        UnprocessedImage.id == unprocessed_image_id
    )
    # get the data
    response_for_image = await db_session.execute(query_for_image)
    image_entry = response_for_image.scalar_one_or_none()
    if not image_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No image found with ID {unprocessed_image_id}",
        )
    # there should only be one entry
    return image_entry

async def get_processed_image_entry_by_id(
    processed_image_id: uuid.UUID,
    db_session: AsyncSession,
    user_id: uuid.UUID
) -> UnprocessedImage:
    """
    Retrieves an unprocessed image by its ID.
    """
    # go find the user with this id
    query_for_user = sqlalchemy.select(User).where(
        User.id == user_id
    )
    response_for_user = await db_session.execute(query_for_user)
    user_entry = response_for_user.scalar_one_or_none()
    # raise an exception if no user exists
    if not user_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found with ID {user_id}",
        )
    # go find the UnprocessedImage where the user_id matches and the image_id matches
    query_for_image = sqlalchemy.select(UnprocessedImage).where(
        UnprocessedImage.user_id == user_entry.id,
        UnprocessedImage.id == processed_image_id
    )
    # get the data
    response_for_image = await db_session.execute(query_for_image)
    image_entry = response_for_image.scalar_one_or_none()
    if not image_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No image found with ID {processed_image_id}",
        )
    # there should only be one entry
    return image_entry


async def get_processed_image_by_id(
    processed_image_id: uuid.UUID,
    db_session: AsyncSession,
    user_id: uuid.UUID
) -> ProcessedImage:
    """
    Retrieves a processed image by its ID.
    """
    # go find the user with this id
    query_for_user = sqlalchemy.select(User).where(
        User.id == user_id
    )
    query_for_user_exists = sqlalchemy.select(User.id).where(
        User.id == user_id
    ).exists()
    response_for_user = await db_session.execute(query_for_user)
    user_entry = response_for_user.scalar_one_or_none()
    # raise an exception if no user exists
    if not user_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found with ID {user_id}",
        )
    # go find the ProcessedImage where the user_id matches and the image_id matches
    query_for_image = sqlalchemy.select(
        ProcessedImage
    ).join(
        UnprocessedImage
    ).where(
        ProcessedImage.id == processed_image_id
    ).where(
        UnprocessedImage.user_id == user_id
    )
    # get the data
    response_for_image = await db_session.execute(query_for_image)
    image_entry = response_for_image.scalar_one_or_none()
    if not image_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No image found with ID {processed_image_id}",
        )
    # there should only be one entry
    return image_entry
