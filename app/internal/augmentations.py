import logging
from datetime import datetime
from math import floor

import numpy
import scipy.ndimage

from app.schemas.logging import LogEntry

# set up logging
logger = logging.getLogger(__name__)

# --- utility function ---
# TODO: move this?

CHANNEL_MAP = {
    'r': 0,
    'g': 1,
    'b': 2,
    'a': 3
}

def split_channels(image_data: numpy.ndarray) -> dict:
    r_channel = image_data[:, :, 0]
    g_channel = image_data[:, :, 1]
    b_channel = image_data[:, :, 2]
    return {
        'r_channel': r_channel,
        'g_channel': g_channel,
        'b_channel': b_channel,
    }

def merge_channels(r_channel: numpy.ndarray, g_channel: numpy.ndarray, b_channel: numpy.ndarray) -> numpy.ndarray:
    merged_array = numpy.stack((r_channel, g_channel, b_channel), axis=-1)
    return merged_array

# --- --- ---

def brighten(image_data: numpy.ndarray, amount: int) -> numpy.ndarray:
    """
    Takes an image and increases the value of every pixel.

    Args:
        image_data (numpy.array): the image data to process.
        amount (int): the percentage amount to increase image brightness.
    Returns:
        numpy.array: The newly processed image.
    """
    value = int(amount/100 * 255)
    for i, row in enumerate(image_data):
        for j, pixel in enumerate(row):
            for k, channel in enumerate(pixel):
                image_data[i][j][k] = min(channel + value, 255)
    return image_data

def channel_swap(image_data: numpy.ndarray, a: str, b: str) -> numpy.ndarray:
    """
    Takes two channels and swaps the values.

    Args:
        image_data (numpy.array): the image data to process.
        a (str): A value for a channel.
        b (str): A value for a channel.
    Returns:
        numpy.array: The newly processed image.
    """
    output_image = image_data.copy()
    if a == b:
        return output_image
    # Get dimensions of image
    width, height = output_image.shape[:2]
    # Get number of channels
    num_channels = output_image.shape[2]
    for i, row in enumerate(output_image):
        for j, pixel in enumerate(row):
            pixel[CHANNEL_MAP[a]], pixel[CHANNEL_MAP[b]] = pixel[CHANNEL_MAP[b]], pixel[CHANNEL_MAP[a]]
    # return the modified array
    return output_image


def cutout(image_data: numpy.ndarray, amount: float) -> numpy.ndarray:
    """
        Takes a subset of contiguous pixels and overwrites the values.
        The cutout is rectangular but not always square.

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
    is_square = True
    # if is_square:
    censor_mask_width = floor(numpy.sqrt(num_pixels))
    censor_mask_height = floor(numpy.sqrt(num_pixels))
    start_x = numpy.random.randint(low=0, high=width - censor_mask_width)
    start_y = numpy.random.randint(low=0, high=height - censor_mask_height)
    end_x = start_x + censor_mask_width
    end_y = start_y + censor_mask_height
    # Generate a set of random colors pixels.
    # apply the random colours to the selected coordinates
    for i in range(start_x, end_x):
        for j in range(start_y, end_y):
            output_image[i][j] = numpy.random.randint(low=0, high=max_val + 1, size=(1, num_channels), dtype=bit_depth)
    # return the modified array
    return output_image

def darken(image_data: numpy.ndarray, amount: int) -> numpy.ndarray:
    """
    Takes an image and increases the value of every pixel.

    Args:
        image_data (numpy.array): the image data to process.
        amount (int): the percentage amount to increase image brightness.
    Returns:
        numpy.array: The newly processed image.
    """
    value = int(amount/100 * 255)
    for i, row in enumerate(image_data):
        for j, pixel in enumerate(row):
            for k, channel in enumerate(pixel):
                image_data[i][j][k] = max(channel - value, 0)
    return image_data


def edge_filter(image_data: numpy.ndarray, image_type: str) -> numpy.ndarray:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.percentile_filter.html#scipy.ndimage.percentile_filter
    # convert to grayscale
    g_image_data = numpy.dot(image_data[...,:3], [0.2989, 0.5870, 0.1140])
    g_image_data = g_image_data.astype('int32')
    sobel_h = scipy.ndimage.sobel(g_image_data, axis=0)
    sobel_v = scipy.ndimage.sobel(g_image_data, axis=1)
    magnitude = numpy.sqrt(sobel_h**2 + sobel_v**2)
    # normalize the magnitude
    max_mag = numpy.max(magnitude)
    if max_mag == 0:
        magnitude_norm_2D = numpy.zeros(magnitude.shape, dtype=image_data.dtype)
    else:
        magnitude_norm_2D = (magnitude * (255.0 / numpy.max(magnitude))).astype(image_data.dtype)
    if image_type == 'edge_map':
        result = numpy.stack([magnitude_norm_2D] * 3, axis=-1)
    else:
        # enhance the edges
        enhance_weight = 0.5
        edge_map_3D = numpy.stack([magnitude_norm_2D] * 3, axis=-1).astype('float32')
        original_3D = image_data[..., :3].astype('float32')
        blended = original_3D + ( edge_map_3D * enhance_weight )
        result = numpy.clip(blended, 0, 255).astype(image_data.dtype)
    return result

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


def gaussian_blur(image_data: numpy.ndarray, amount: int) -> numpy.ndarray:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter.html#scipy.ndimage.gaussian_filter
    sigma = amount / 100
    channel_dict = split_channels(image_data)
    result_b = scipy.ndimage.gaussian_filter(channel_dict['b_channel'], sigma=sigma).astype(image_data.dtype)
    result_r = scipy.ndimage.gaussian_filter(channel_dict['r_channel'], sigma=sigma).astype(image_data.dtype)
    result_g = scipy.ndimage.gaussian_filter(channel_dict['g_channel'], sigma=sigma).astype(image_data.dtype)
    result = merge_channels(
        r_channel=result_r,
        g_channel=result_g,
        b_channel=result_b,
    )
    return result

def invert(image_data: numpy.ndarray) -> numpy.ndarray:
    for i, row in enumerate(image_data):
        for j, pixel in enumerate(row):
            for k, channel in enumerate(pixel):
                image_data[i][j][k] = max(255 - channel, 0)
    return image_data

def max_filter(image_data: numpy.ndarray, size: int) -> numpy.ndarray:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.maximum_filter.html#scipy.ndimage.maximum_filter
    channel_dict = split_channels(image_data)
    result_r = scipy.ndimage.maximum_filter(channel_dict['r_channel'], size=size).astype(image_data.dtype)
    result_g = scipy.ndimage.maximum_filter(channel_dict['g_channel'], size=size).astype(image_data.dtype)
    result_b = scipy.ndimage.maximum_filter(channel_dict['b_channel'], size=size).astype(image_data.dtype)
    result = merge_channels(
        r_channel=result_r,
        g_channel=result_g,
        b_channel=result_b,
    )
    return result

def min_filter(image_data: numpy.ndarray, size: int) -> numpy.ndarray:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.minimum_filter.html#scipy.ndimage.minimum_filter
    channel_dict = split_channels(image_data)
    result_b = scipy.ndimage.minimum_filter(channel_dict['b_channel'], size=size).astype(image_data.dtype)
    result_r = scipy.ndimage.minimum_filter(channel_dict['r_channel'], size=size).astype(image_data.dtype)
    result_g = scipy.ndimage.minimum_filter(channel_dict['g_channel'], size=size).astype(image_data.dtype)
    result = merge_channels(
        r_channel=result_r,
        g_channel=result_g,
        b_channel=result_b,
    )
    return result

def mute_channel(image_data: numpy.ndarray, channel: str) -> numpy.ndarray:
    for i, row in enumerate(image_data):
        for j, pixel in enumerate(row):
            image_data[i][j][CHANNEL_MAP[channel]] = 0
    return image_data

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


def percentile_filter(image_data: numpy.ndarray, percentile: int, size: int) -> numpy.ndarray:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.percentile_filter.html#scipy.ndimage.percentile_filter
    channel_dict = split_channels(image_data)
    result_r = scipy.ndimage.percentile_filter(channel_dict['r_channel'], percentile=percentile, size=size).astype(image_data.dtype)
    result_g = scipy.ndimage.percentile_filter(channel_dict['g_channel'], percentile=percentile, size=size).astype(image_data.dtype)
    result_b = scipy.ndimage.percentile_filter(channel_dict['b_channel'], percentile=percentile, size=size).astype(image_data.dtype)
    result = merge_channels(
        r_channel=result_r,
        g_channel=result_g,
        b_channel=result_b,
    )
    return result

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

def tint(image_data: numpy.ndarray, channel: str, amount: float) -> numpy.ndarray:
    for i, row in enumerate(image_data):
        for j, pixel in enumerate(row):
            for k, c in enumerate(pixel):
                channel_to_change = CHANNEL_MAP[channel]
                if k == channel_to_change:
                    image_data[i][j][k] = min(int(c + (c * amount/2)), 255)
                else:
                    image_data[i][j][k] = max(int(c - (c * amount/2)), 0)
    return image_data

def uniform_blur(image_data: numpy.ndarray, size: int) -> numpy.ndarray:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.uniform_filter.html#scipy.ndimage.uniform_filter
    channel_dict = split_channels(image_data)
    result_r = scipy.ndimage.uniform_filter(channel_dict['r_channel'], size=size).astype(image_data.dtype)
    result_g = scipy.ndimage.uniform_filter(channel_dict['g_channel'], size=size).astype(image_data.dtype)
    result_b = scipy.ndimage.uniform_filter(channel_dict['b_channel'], size=size).astype(image_data.dtype)
    result = merge_channels(
        r_channel=result_r,
        g_channel=result_g,
        b_channel=result_b,
    )
    return result


def zoom(image_data: numpy.ndarray, amount: float) -> numpy.ndarray:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.zoom.html#scipy.ndimage.zoom
    width, height = image_data.shape[:2]
    channel_dict = split_channels(image_data)
    result_r = scipy.ndimage.zoom(channel_dict['r_channel'], zoom=amount).astype(
        image_data.dtype)
    result_g = scipy.ndimage.zoom(channel_dict['g_channel'], zoom=amount).astype(
        image_data.dtype)
    result_b = scipy.ndimage.zoom(channel_dict['b_channel'], zoom=amount).astype(
        image_data.dtype)
    result = merge_channels(
        r_channel=result_r,
        g_channel=result_g,
        b_channel=result_b,
    )
    # TODO: random zoom point?
    result = result[0:width, 0:height]
    return result

# TODO: Shear
# TODO: Perspective Warp
# TODO: Elastic Transformation
# TODO: Contrast
# TODO: Saturate
# TODO: Color Jitter
# TODO: Grayscale
# TODO: Solarize
# TODO: Grid Mask