import numpy
import pytest
from PIL import Image
import io

from app.internal.file_handling import translate_file_to_numpy_array, InvalidImageFileError

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

def test_translate_file_to_numpy_array():
    """
    GIVEN valid image bytes
    WHEN translate_file_to_numpy_array is called
    THEN the correct numpy array is returned.
    """
    input_image_bytes = create_dummy_image_bytes()
    expected_output = numpy.array( [
        [[255, 0, 0], [0,255, 0]],
        [[0, 0, 255], [255, 0, 0]]
    ], dtype=numpy.uint8)
    calculated_output = translate_file_to_numpy_array(input_image_bytes)
    assert numpy.array_equal(expected_output, calculated_output)

def test_translate_file_to_numpy_array_raises_InvalidImageFileError():
    """
    GIVEN an invalid image bytes
    WHEN translate_file_to_numpy_array is called
    THEN it should raise an error
    """
    input_image_bytes = b'this is not a valid image bytes'
    with pytest.raises(InvalidImageFileError):
        translate_file_to_numpy_array(input_image_bytes)

