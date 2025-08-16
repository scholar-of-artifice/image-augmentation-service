import numpy
from PIL import Image
import io

from app.internal.file_handling import translate_file_to_numpy_array

def create_dummy_image_bytes() -> bytes:
    """
        Helper function that creates a dummy image byte array for testing.
    """
    # Create in memory byte buffer
    buffer = io.BytesIO()
    # Create a simple 2x2 RGB image
    array = numpy.array( [
        [[255, 0, 0], [0,255, 0]],
        [[0, 0, 255], [255, 0, 0]]
    ], dtype=numpy.uint8)
    img = Image.fromarray(array)
    # save the image to the buffer in png format
    img.save(buffer, format='PNG')
    # return the byte content
    return buffer.getvalue()
