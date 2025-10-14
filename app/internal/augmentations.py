import logging
from datetime import datetime

import numpy
import scipy.ndimage

from app.schemas.logging import LogEntry

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
        date_time=datetime.now(),
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
        date_time=datetime.now(),
        event="rotate",
        details="Processing rotate.",
    )
    logger.info(log_data.model_dump_json())
    return scipy.ndimage.rotate(input=image_data, angle=angle, reshape=False)

def flip(image_data: numpy.ndarray, axis: str) -> numpy.ndarray:
    """
    Flips image along the specified axis.

    Args:
        image_data (numpy.array): the image data to process.
        axis (string): 'x' makes the image upside down. 'y' makes a mirror image.
    Returns:
        numpy.array: The newly processed image.
    """
    if axis == 'x':
        return numpy.flipud(image_data)
    else:
        return numpy.fliplr(image_data)


def rainbow_noise(image_data: numpy.ndarray, amount: float) -> numpy.ndarray:
    """
    Applies random noise to a percentage of pixels in the image.
    Takes n randomly selected pixels and overwrites the pixel value.

    Args:
        image_data (numpy.array): the image data to process.
        amount (float): The percentage of pixels to replace with noise, as a float between 0.0 and 1.0 (e.g., 0.1 for 10%).
    Returns:
        numpy.array: The newly processed image.
    """
    output_image = image_data.copy()
    # Get dimensions of image
    width, height = output_image.shape[:2]
    # Get number of channels
    num_channels = output_image.shape[2]
    # Get the bit depth of the image
    bit_depth = output_image.dtype
    max_val = numpy.iinfo(bit_depth).max
    # Calculate the number of pixels to change
    num_pixels = int(amount * height * width)
    # Generate a random set of coordinates
    rows = numpy.random.randint(low=0, high=height, size=num_pixels)
    columns = numpy.random.randint(low=0, high=width, size=num_pixels)
    # Generate a set of random colors pixels.
    random_colours = numpy.random.randint(low=0, high=max_val + 1, size=(num_pixels, num_channels), dtype=bit_depth)
    # apply the random colours to the selected coordinates
    output_image[rows, columns] = random_colours
    # return the modified array
    return output_image


def salt_noise(image_data: numpy.ndarray, amount: float) -> numpy.ndarray:
    """
    Applies random noise to a percentage of pixels in the image.
    Takes n randomly selected pixels and overwrites the pixel as white.

    Args:
        image_data (numpy.array): the image data to process.
        amount (float): The percentage of pixels to replace with noise, as a float between 0.0 and 1.0 (e.g., 0.1 for 10%).
    Returns:
        numpy.array: The newly processed image.
    """
    output_image = image_data.copy()
    # Get dimensions of image
    width, height = output_image.shape[:2]
    # Get number of channels
    num_channels = output_image.shape[2]
    # Get the bit depth of the image
    bit_depth = output_image.dtype
    max_val = numpy.iinfo(bit_depth).max
    # Calculate the number of pixels to change
    num_pixels = int(amount * height * width)
    # Generate a random set of coordinates
    rows = numpy.random.randint(low=0, high=height, size=num_pixels)
    columns = numpy.random.randint(low=0, high=width, size=num_pixels)
    # Generate a set of random colors pixels.
    random_white = numpy.random.randint(low=max_val, high=max_val + 1, size=(num_pixels, num_channels), dtype=bit_depth)
    # apply the random colours to the selected coordinates
    output_image[rows, columns] = random_white
    # return the modified array
    return output_image


def pepper_noise(image_data: numpy.ndarray, amount: float) -> numpy.ndarray:
    """
    Applies random noise to a percentage of pixels in the image.
    Takes n randomly selected pixels and overwrites the pixel as white.

    Args:
        image_data (numpy.array): the image data to process.
        amount (float): The percentage of pixels to replace with noise, as a float between 0.0 and 1.0 (e.g., 0.1 for 10%).
    Returns:
        numpy.array: The newly processed image.
    """
    output_image = image_data.copy()
    # Get dimensions of image
    width, height = output_image.shape[:2]
    # Get number of channels
    num_channels = output_image.shape[2]
    # Get the bit depth of the image
    bit_depth = output_image.dtype
    max_val = numpy.iinfo(bit_depth).max
    # Calculate the number of pixels to change
    num_pixels = int(amount * height * width)
    # Generate a random set of coordinates
    rows = numpy.random.randint(low=0, high=height, size=num_pixels)
    columns = numpy.random.randint(low=0, high=width, size=num_pixels)
    # Generate a set of random colors pixels.
    random_black = numpy.random.randint(low=0, high=1, size=(num_pixels, num_channels), dtype=bit_depth)
    # apply the random colours to the selected coordinates
    output_image[rows, columns] = random_black
    # return the modified array
    return output_image