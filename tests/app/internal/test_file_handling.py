import numpy
import pytest
from app.internal.file_handling import (
    translate_file_to_numpy_array,
    write_numpy_array_to_image_file,
    InvalidImageFileError,
    create_file_name,
    VOLUME_PATHS
)
from tests.app.helperfunc.helperfunc import create_dummy_numpy_array, create_dummy_image_bytes

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

def test_write_numpy_array_to_image_file_to_invalid_file_path_raises_ValueError(tmp_path, monkeypatch):
    """
        GIVEN a numpy array with valid image data
        WHEN write_numpy_array_to_image_file is called
        THEN an exception is raised.
    """
    # create a temporary directory for the 'unprocessed' image
    unprocessed_dir = tmp_path / "unprocessed"
    unprocessed_dir.mkdir()
    # temporarily point the volume name to the test directory
    monkeypatch.setitem(VOLUME_PATHS, "unprocessed_image_data", unprocessed_dir)
    # execute the test
    input_numpy_array = create_dummy_numpy_array()
    file_name = 'test_image'
    destination = 'this_destination_does_not_exist'
    expected_file_path = (unprocessed_dir / f"{file_name}.png")
    with pytest.raises(ValueError) as e:
        write_numpy_array_to_image_file(data=input_numpy_array, file_name=file_name, destination_volume=destination )

def test_create_file_name_returns_a_string():
    """
        GIVEN no arguments
        WHEN create_file_name is called
        THEN it should return a string
    """
    assert isinstance(create_file_name(), str)

def test_create_file_name_returns_a_non_empty_string():
    """
        GIVEN no arguments
        WHEN create_file_name is called
        THEN it should return a non-empty string
    """
    calculated_file_name = create_file_name()
    assert create_file_name() != 'wow_a_file.png'

def test_create_file_name_returns_a_nonspecific_string():
    """
        GIVEN no arguments
        WHEN create_file_name is called
        THEN it should return a non-empty string
    """
    calculated_file_name = create_file_name()
    assert create_file_name() != 'wow_an_oddly_specific_filename.png'

def test_create_file_name_returns_a_different_values_per_function_call():
    """
        GIVEN no arguments
        WHEN create_file_name is called twice
        THEN it should return different values
    """
    calculated_file_name_A = create_file_name()
    calculated_file_name_B = create_file_name()
    assert(calculated_file_name_A != calculated_file_name_B)