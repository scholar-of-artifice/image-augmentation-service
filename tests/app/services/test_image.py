from app.models.image_api.upload import UploadRequestBody, ShiftArguments, RotateArguments
from app.services.image import process_and_save_image

import pytest

pytestmark = pytest.mark.asyncio

async def test_process_and_save_image_with_shift_arguments_succeeds(mocker):
    """
        GIVEN a valid UploadFile and a UploadRequestBody with 'shift' arguments
        AND all helper functions (dependencies) are mocked
        WHEN the process_and_save_image service is called
        THEN the shift_processor is called with the correct arguments
        AND the file_writer is called twice
        AND the rotate_processor is NOT called
        AND a valid ImageProcessResponse is returned
    """
    # mock the dependencies
    mock_file_translator = mocker.MagicMock(return_value="numpy_array_data")
    mock_file_writer = mocker.MagicMock(side_effect=["/path/original.jpg", "/path/shifted.jpg"])
    mock_filename_creator = mocker.MagicMock(return_value="new_filename.jpg")
    mock_shift_processor = mocker.MagicMock(return_value="shifted_numpy_array")
    mock_rotate_processor = mocker.MagicMock()