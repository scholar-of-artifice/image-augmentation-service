"""
This module contains a number of functions for creating, reading and deleting directories.
"""
import uuid
import numpy
from PIL import Image, UnidentifiedImageError
from app.exceptions import (
    UserNotFound,
    UserDirectoryAlreadyExists,
    ImageAlreadyExists,
    ImageDirectoryAlreadyExists,
    ImageNotFound
)
import io
from pathlib import Path
from app.config import settings
from app.internal.file_handling import translate_file_to_numpy_array

# Define a mapping from volume names to the in-container paths for easy lookup
VOLUME_PATHS = {
    "unprocessed_image_data": settings.UNPROCESSED_IMAGE_PATH,
    "processed_image_data": settings.PROCESSED_IMAGE_PATH,
}

async def create_unprocessed_user_directory(
        user_id: uuid.UUID,
) -> Path:
    """
    Create an unprocessed image directory.
    """
    # create the path object
    user_dir_path = VOLUME_PATHS["unprocessed_image_data"] / str(user_id)
    # check if subdirectory exists
    try:
        user_dir_path.mkdir(parents=False, exist_ok=False)
        return user_dir_path
    except FileExistsError:
        raise UserDirectoryAlreadyExists(
            f"{user_dir_path} already exists."
        )


async def delete_unprocessed_user_directory(
        user_id: uuid.UUID,
) -> None:
    """
    Delete the entire subdirectory of unprocessed images for a particular user.
    """
    # TODO: check if subdirectory exists
    # /image-augmentation-service/data/images/unprocessed/{user_id}/
    # TODO: delete subdirectory and all internal contents
    return None

async def write_unprocessed_image(
        image_data: numpy.ndarray,
        user_id: uuid.UUID,
        storage_filename: str,
) -> Path:
    """
    Write an unprocessed image file to the filesystem.
    """
    # check if the file exists
    image_filepath = VOLUME_PATHS["unprocessed_image_data"] / str(user_id) / storage_filename
    try:
        # convert the numpy array to a Pillow Image object.
        image = Image.fromarray(
            obj=image_data,
        )
        # save the image object to the save location in PNG format
        image.save(
            fp= str(image_filepath),
            format='PNG'
        )
        return image_filepath
    except FileExistsError:
        raise ImageAlreadyExists(
            f"{image_filepath} already exists."
        )


async def create_processed_user_directory(
        user_id: uuid.UUID,
) -> Path:
    """
    Create a processed image directory.
    """
    # create the path object
    user_dir_path = VOLUME_PATHS["processed_image_data"] / str(user_id)
    # check if subdirectory exists
    try:
        user_dir_path.mkdir(parents=False, exist_ok=False)
        return user_dir_path
    except FileExistsError:
        raise UserDirectoryAlreadyExists(
            f"{user_dir_path} already exists."
        )


async def delete_processed_user_directory(
        user_id: uuid.UUID,
) -> None:
    """
    Delete the entire subdirectory of processed images for a particular user.
    """
    # TODO: check if subdirectory exists
    # /image-augmentation-service/data/images/processed/{user_id}/
    # TODO: delete subdirectory and all internal contents
    return None


async def create_processed_image_directory(
        user_id: uuid.UUID,
        image_id: uuid.UUID,
) -> None:
    """
    Create a processed image directory.
    """
    user_dir_path = VOLUME_PATHS["processed_image_data"] / str(user_id) / str(image_id)
    # check if subdirectory exists
    try:
        user_dir_path.mkdir(parents=False, exist_ok=False)
        return user_dir_path
    except FileExistsError:
        raise ImageDirectoryAlreadyExists(
            f"{user_dir_path} already exists."
        )


async def delete_processed_image_directory(
        user_id: uuid.UUID,
        image_id: uuid.UUID,
) -> None:
    """
    Delete a processed image directory.
    """
    # TODO: check if subdirectory exists
    # /image-augmentation-service/data/images/processed/{user_id}/{image_id}
    # TODO: delete subdirectory
    return None