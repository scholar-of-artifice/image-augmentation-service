import numpy


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
    if direction == 'up':
        return numpy.roll(image_data, -distance, axis=0)
    elif direction == 'down':
        return numpy.roll(image_data, distance, axis=0)
    elif direction == 'left':
        return numpy.roll(image_data, -distance, axis=1)
    elif direction == 'right':
        return numpy.roll(image_data, distance, axis=1)
    else:
        return image_data  # do nothing
