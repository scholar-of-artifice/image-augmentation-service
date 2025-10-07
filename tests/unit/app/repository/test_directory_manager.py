import uuid
from unittest.mock import MagicMock

import pytest
from pathlib import Path
from app.repository.directory_manager import (
VOLUME_PATHS,
create_unprocessed_user_directory,
write_unprocessed_image
)
import numpy
pytestmark = pytest.mark.asyncio

async def test_VOLUME_PATHS_has_correct_structure():
    """
    GIVEN a VOLUME_PATHS
    WHEN the VOLUME_PATHS structure is read
    THEN it should have the correct structure
    """
    assert VOLUME_PATHS == {
        "unprocessed_image_data": Path('/image-augmentation-service/data/images/unprocessed'),
        "processed_image_data": Path('/image-augmentation-service/data/images/processed'),
    }

async def test_create_unprocessed_user_directory_creates_new_directory(mocker):
    """
    GIVEN a subdirectory for a user does not exist
    WHEN create_unprocessed_user_directory is called
    THEN it should create the new directory
    """
    fake_user_id = uuid.uuid4()
    expected_path = VOLUME_PATHS["unprocessed_image_data"] / str(fake_user_id)
    # mock the file system
    mock_mkdir = mocker.patch("pathlib.Path.mkdir")
    # call the function
    new_path = await create_unprocessed_user_directory(user_id=fake_user_id)
    # do checks
    assert new_path == expected_path

async def test_write_unprocessed_image_success(mocker):
    """
    GIVEN an image
    AND a user_id
    AND a storage_filename
    WHEN write_unprocessed_image is called
    THEN it should create the new directory
    """
    # make fake image data
    fake_image_data = numpy.random.random((4, 4, 3))
    fake_user_id = uuid.uuid4()
    fake_storage_filename = f"{uuid.uuid4()}.png"
    #
    mock_image_instance = MagicMock()
    mock_fromarray = mocker.patch(
        "app.repository.directory_manager.Image.fromarray",
        return_value=mock_image_instance
    )
    # call the funciton
    result_path = await write_unprocessed_image(
        image_data=fake_image_data,
        user_id=fake_user_id,
        storage_filename=fake_storage_filename,
    )
    expected_path = VOLUME_PATHS["unprocessed_image_data"] / str(fake_user_id) / fake_storage_filename
    mock_fromarray.assert_called_once_with(obj= fake_image_data)
    mock_image_instance.save.assert_called_once_with(
        fp=expected_path,
        format='PNG'
    )
    assert result_path == expected_path

