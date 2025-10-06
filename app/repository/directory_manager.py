"""
This module contains a number of functions for creating, reading and deleting directories.
"""
import uuid


async def create_unprocessed_user_directory(
        user_id: uuid.UUID,
) -> None:
    """
    Create an unprocessed image directory.
    """
    # TODO: check if subdirectory exists
    # /image-augmentation-service/data/images/unprocessed/{user_id}/
    # TODO: create subdirectory
    return None


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


async def create_processed_user_directory(
        user_id: uuid.UUID,
) -> None:
    """
    Create a processed image directory.
    """
    # TODO: check if subdirectory exists
    # /image-augmentation-service/data/images/processed/{user_id}/
    # TODO: create subdirectory
    return None


async def delete_processed_user_directory(
        user_id: uuid.UUID,
) -> None:
    """
    Delete a processed image directory.
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
    # TODO: check if subdirectory exists
    # /image-augmentation-service/data/images/processed/{user_id}/{image_id}
    # TODO: create subdirectory
    return None


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