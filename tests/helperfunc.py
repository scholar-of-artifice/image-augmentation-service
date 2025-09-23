import io
from contextlib import contextmanager
from pathlib import Path
from typing import ContextManager

import numpy
from PIL import Image, UnidentifiedImageError

__current_directory = Path(__file__).parent
TESTS_DIR = __current_directory.parent.parent

def create_dummy_image_bytes() -> bytes:
    """
        Helper function that creates a dummy image byte array for testing.

        Returns:
            bytes: dummy image byte array
    """
    # Create in memory byte buffer
    buffer = io.BytesIO()
    # Create a simple 3x3 RGB image
    array = numpy.array( [
        [[255, 0, 0], [0,255, 0], [0, 0, 255]],
        [[255, 255, 255], [127, 127, 127], [0, 0, 0]],
        [[127, 0, 0], [0,127, 0], [0, 0, 127]],
    ], dtype=numpy.uint8)
    img = Image.fromarray(array)
    # save the image to the buffer in png format
    img.save(buffer, format='PNG')
    # return the byte content
    return buffer.getvalue()

def create_dummy_numpy_array() -> numpy.ndarray:
    """
        Helper function that creates a dummy numpy array for testing.
        Represents a potential image with RGB values.

        Returns:
            numpy.ndarray: dummy numpy array
    """
    return numpy.array([
        [[255, 0, 0], [0,255, 0], [0, 0, 255]],
        [[255, 255, 255], [127, 127, 127], [0, 0, 0]],
        [[127, 0, 0], [0,127, 0], [0, 0, 127]],
    ], dtype=numpy.uint8)

def get_test_image_path() -> Path:
    """
        Helper function that returns the path to the test image file.

        Returns:
            Path: test image path
    """
    return TESTS_DIR / "data" / "test_image.png"

@contextmanager
def get_test_image() -> ContextManager[bytes]:
    """
        Safely opens a test image and yields its raw byte content.

        This function is a context manager that handles opening and closing the image file.

        Raises:
            FileNotFoundError: if test image file does not exist
            ValueError: if the file cannot be identified as an valid image
        Yields:

    """
    file_path = get_test_image_path()
    try:
        with Image.open(file_path) as img:
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            yield buffer.getvalue()
    except FileNotFoundError:
        raise FileNotFoundError("test image file does not exist")
    except UnidentifiedImageError:
        raise ValueError(f"{file_path} is not a valid image.")
