import uuid

import pytest
from pathlib import Path
from app.repository.directory_manager import (
VOLUME_PATHS,
create_unprocessed_user_directory
)

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
