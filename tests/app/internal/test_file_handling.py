import numpy
import pytest
from PIL import Image
import io
import os

from app.internal.file_handling import translate_file_to_numpy_array, write_numpy_array_to_image_file, InvalidImageFileError, create_file_name

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

def create_dummy_numpy_array() -> numpy.ndarray:
    """
        Helper function that creates a dummy numpy array for testing.
        Represents a potential image with RGB values.
    """
    return numpy.array([
        [[255, 0, 0], [0,255, 0], [0,255, 0], [0,255, 0]],
        [[0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 255]],
        [[0, 0, 255], [255, 0, 255], [255, 0, 0], [0, 0, 0]],
        [[0, 255, 255], [255, 255, 255], [0, 0, 0], [255, 255, 0]],
    ], dtype=numpy.uint8)

def create_write_directory():
    # ensure the target director exists...
    os.makedirs('app/_tmp', exist_ok=True)

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

def test_write_numpy_array_to_image_file():
    """
    GIVEN a numpy array with valid image data
    WHEN write_numpy_array_to_image_file is called
    THEN a file_path_is_returned.
    """
    # setup preconditions
    create_write_directory()
    input_numpy_array = create_dummy_numpy_array()
    #
    calculated_file_path = write_numpy_array_to_image_file(data=input_numpy_array, file_name='wow_a_file' )
    #
    expected_file_path = 'app/_tmp/wow_a_file.png'
    assert numpy.array_equal(expected_file_path, calculated_file_path)

def test_create_file_name_returns_a_non_empty_string():
    """
    GIVEN no arguments
    WHEN create_file_name is called
    THEN it should return a file name
    """
    calculated_file_name = create_file_name()
    assert calculated_file_name != 'wow_a_file.png'
    assert calculated_file_name is not None
    assert calculated_file_name != ""
    assert isinstance(calculated_file_name, str) is True

def test_create_file_name_returns_a_different_values_per_function_call():
    """
    GIVEN no arguments
    WHEN create_file_name is called twice
    THEN it should return different values
    """
    calculated_file_name_A = create_file_name()
    calculated_file_name_B = create_file_name()
    assert(calculated_file_name_A != calculated_file_name_B)