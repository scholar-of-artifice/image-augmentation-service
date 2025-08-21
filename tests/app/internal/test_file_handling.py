import numpy
import pytest
from PIL import Image
import io
import os

from app.internal.file_handling import translate_file_to_numpy_array, write_numpy_array_to_image_file, \
    InvalidImageFileError, create_file_name, VOLUME_PATHS


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
    """
    return numpy.array([
        [[255, 0, 0], [0,255, 0], [0,255, 0], [0,255, 0]],
        [[0, 0, 0], [255, 0, 0], [255, 0, 0], [255, 0, 255]],
        [[0, 0, 255], [255, 0, 255], [255, 0, 0], [0, 0, 0]],
        [[0, 255, 255], [255, 255, 255], [0, 0, 0], [255, 255, 0]],
    ], dtype=numpy.uint8)

def create_write_directory():
    """
        Helper function that creates a dummy directory for testing.
    """
    # ensure the target director exists...
    os.makedirs('app/_tmp', exist_ok=True)

def test_translate_file_to_numpy_array_creates_correct_result_when_given_valid_image_data():
    """
        GIVEN valid image bytes
        WHEN translate_file_to_numpy_array is called
        THEN the correct numpy array is returned.
    """
    input_image_bytes = create_dummy_image_bytes()
    expected_output = numpy.array( object= [
        [[255, 0, 0], [0,255, 0], [0, 0, 255]],
        [[255, 255, 255], [127, 127, 127], [0, 0, 0]],
        [[127, 0, 0], [0,127, 0], [0, 0, 127]],
    ], dtype=numpy.uint8 )
    calculated_output = translate_file_to_numpy_array( content= input_image_bytes )
    assert numpy.array_equal(expected_output, calculated_output)

def test_translate_file_to_numpy_array_raises_InvalidImageFileError_when_given_invalid_image_data():
    """
        GIVEN invalid image bytes
        WHEN translate_file_to_numpy_array is called
        THEN an exception is raised.
    """
    # make bad data
    input_image_bytes = b'this is not a valid image bytes'
    # assert that calling the function raises an error
    with pytest.raises(InvalidImageFileError):
        translate_file_to_numpy_array( content= input_image_bytes )

def test_write_numpy_array_to_image_file(tmp_path, monkeypatch):
    """
    GIVEN a numpy array with valid image data
    WHEN write_numpy_array_to_image_file is called
    THEN a file_path_is_returned.
    """
    # create a temporary directory for the 'unprocessed' image
    unprocessed_dir = tmp_path / "unprocessed"
    unprocessed_dir.mkdir()
    # temporarily point the volume name to the test directory
    monkeypatch.setitem(VOLUME_PATHS, "unprocessed_image_data", unprocessed_dir)
    # execute the test
    input_numpy_array = create_dummy_numpy_array()
    file_name = 'test_image'
    destination = 'unprocessed_image_data'
    expected_file_path = (unprocessed_dir / f"{file_name}.png")
    calculated_file_path = write_numpy_array_to_image_file(data=input_numpy_array, file_name=file_name, destination_volume=destination )
    #
    assert str(expected_file_path) == str(calculated_file_path)
    assert (expected_file_path).exists()

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