import numpy
from PIL import Image
import io
from pathlib import Path
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
