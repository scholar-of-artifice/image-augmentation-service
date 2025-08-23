import numpy
import scipy.ndimage
from app.models.logging import LogEntry
import logging

# set up logging
logger = logging.getLogger(__name__)

def shift(image_data: numpy.ndarray, direction: str, distance: int) -> numpy.ndarray:
    """
    Translate an image by a specified distance (in pixels).
    The image wraps as pixels go beyond the image frame.

    Args:
        image_data (numpy.array): the image data to process.
        direction (str): the direction of the shift
        distance (int): the amount of the shift in pixels
    Returns:
        numpy.array: The newly processed image.
    """
    if not isinstance(image_data, numpy.ndarray) or image_data.ndim < 2:
        raise TypeError(
            "image_data must be a numpy.ndarray with at least 2 dimensions.")
    if not isinstance(direction, str):
        raise TypeError(
            "direction must be a string.")
    if not isinstance(distance, int):
        raise TypeError(
            "distance must be an integer.")
    direction_map = {
        # direct -> (shift_direction, axis)
        'up': (-1, 0),
        'down': (1, 0),
        'left': (-1, 1),
        'right': (1, 1),
    }
    if direction not in direction_map:
        raise ValueError(
            f"Invalid direction: '{direction}'. Must be 'up', 'down', 'left' or 'right'.")
    log_data = LogEntry(
        event="shift",
        details="Processing shift.",
    )
    logger.info(log_data.model_dump_json())
    shift_direction, axis = direction_map[direction]
    return numpy.roll(image_data, shift_direction * distance, axis=axis)


def rotate(image_data: numpy.ndarray, angle: int) -> numpy.ndarray:
    """
    Rotates and image by a specified number of degrees.

    Args:
        image_data (numpy.array): the image data to process.
        angle (int): value as degrees <example: 45º is 45>
    Returns:
        numpy.array: The newly processed image.
    """
    if not isinstance(image_data, numpy.ndarray) or image_data.ndim < 2:
        raise TypeError(
            "image_data must be a numpy.ndarray with at least 2 dimensions.")
    if not isinstance(angle, int):
        raise TypeError("angle must be an integer")
    if angle == 0:
        return image_data
    log_data = LogEntry(
        event="rotate",
        details="Processing rotate.",
    )
    logger.info(log_data.model_dump_json())
    return scipy.ndimage.rotate(input=image_data, angle=angle, reshape=False)
