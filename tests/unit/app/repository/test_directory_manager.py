import pytest
from pathlib import Path
from app.repository.directory_manager import (
VOLUME_PATHS
)

def test_VOLUME_PATHS_has_correct_structure():
    """
    GIVEN a VOLUME_PATHS
    WHEN the VOLUME_PATHS structure is read
    THEN it should have the correct structure
    """
    assert VOLUME_PATHS == {
        "unprocessed_image_data": Path('/image-augmentation-service/data/images/unprocessed'),
        "processed_image_data": Path('/image-augmentation-service/data/images/processed'),
    }
