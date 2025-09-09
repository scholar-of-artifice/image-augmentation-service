import pytest
from app.internal.file_handling import (
    write_numpy_array_to_image_file,
    VOLUME_PATHS
)
from tests.helperfunc import create_dummy_numpy_array


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
