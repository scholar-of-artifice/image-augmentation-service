import uuid
from unittest.mock import AsyncMock

import pytest
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.file_handling import InvalidImageFileError
from app.schemas.image import RotateArguments, ShiftArguments, UploadRequestBody
from app.services.image import process_and_save_image

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
    # mock the synchronous dependencies
    mock_file_translator = mocker.MagicMock(return_value="numpy_array_data")
    mock_file_writer = mocker.MagicMock(
        side_effect=["/path/original.jpg", "/path/shifted.jpg"]
    )
    mock_filename_creator = mocker.MagicMock(return_value="new_filename.jpg")
    mock_shift_processor = mocker.MagicMock(return_value="shifted_numpy_array")
    mock_rotate_processor = mocker.MagicMock()
    sample_user_id = uuid.uuid4()
    # mock the asynchronous dependencies
    mock_db_session = AsyncMock(spec=AsyncSession)
    # create mock input data for the service function
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test.jpg"
    # configure the return value directly on the AsyncMock's method
    mock_file.read.return_value = b"fake_image_bytes"
    # inputs for process_and_save_image
    shift_args = ShiftArguments(processing="shift", direction="up", distance=100)
    validated_data = UploadRequestBody(arguments=shift_args)
    # call the service with injected dependencies
    result = await process_and_save_image(
        file=mock_file,
        validated_data=validated_data,
        file_translator=mock_file_translator,
        file_writer=mock_file_writer,
        filename_creator=mock_filename_creator,
        shift_processor=mock_shift_processor,
        rotate_processor=mock_rotate_processor,
        db_session=mock_db_session,
        user_id=sample_user_id,
    )
    # assert the correct functions were called
    mock_file_translator.assert_called_once_with(b"fake_image_bytes")
    mock_shift_processor.assert_called_once_with(
        image_data="numpy_array_data", direction="up", distance=100
    )
    mock_rotate_processor.assert_not_called()
    assert mock_file_writer.call_count == 2
    # assert the results were correct
    assert result.original_stored_file_path == "/path/original.jpg"
    assert result.new_stored_file_path == "/path/shifted.jpg"
    assert result.body == validated_data


async def test_process_and_save_image_with_rotate_arguments_succeeds(mocker):
    """
    GIVEN a valid UploadFile and a UploadRequestBody with 'rotate' arguments
    AND all helper functions (dependencies) are mocked
    WHEN the process_and_save_image service is called
    THEN the rotate_processor is called with the correct arguments
    AND the file_writer is called twice
    AND the rotate_processor is NOT called
    AND a valid ImageProcessResponse is returned
    """
    # mock the synchronous dependencies
    mock_file_translator = mocker.MagicMock(return_value="numpy_array_data")
    mock_file_writer = mocker.MagicMock(
        side_effect=["/path/original.jpg", "/path/rotated.jpg"]
    )
    mock_filename_creator = mocker.MagicMock(return_value="new_filename.jpg")
    mock_shift_processor = mocker.MagicMock()
    mock_rotate_processor = mocker.MagicMock(return_value="rotated_numpy_array")
    sample_user_id = uuid.uuid4()
    # mock the asynchronous dependencies
    mock_db_session = AsyncMock(spec=AsyncSession)
    # create mock input data for the service function
    mock_file = AsyncMock(spec=UploadFile)
    mock_file.filename = "test.jpg"
    # configure the return value directly on the AsyncMock's method
    mock_file.read.return_value = b"fake_image_bytes"
    # inputs for process_and_save_image
    rotate_args = RotateArguments(processing="rotate", angle=100)
    validated_data = UploadRequestBody(arguments=rotate_args)
    # call the service with injected dependencies
    result = await process_and_save_image(
        file=mock_file,
        validated_data=validated_data,
        file_translator=mock_file_translator,
        file_writer=mock_file_writer,
        filename_creator=mock_filename_creator,
        shift_processor=mock_shift_processor,
        rotate_processor=mock_rotate_processor,
        db_session=mock_db_session,
        user_id=sample_user_id,
    )
    # assert the correct functions were called
    mock_file_translator.assert_called_once_with(b"fake_image_bytes")
    mock_rotate_processor.assert_called_once_with(
        image_data="numpy_array_data", angle=100
    )
    mock_shift_processor.assert_not_called()
    assert mock_file_writer.call_count == 2
    # assert the results were correct
    assert result.original_stored_file_path == "/path/original.jpg"
    assert result.new_stored_file_path == "/path/rotated.jpg"
    assert result.body == validated_data


async def test_process_and_save_image_raises_error_on_invalid_file(mocker):
    """
    GIVEN an upload file that is not a valid image
    AND the file_translator is mocked to raise an InvalidImageFileError
    WHEN the process_and_save_image service is called
    THEN an InvalidImageFileError is raised
    """
    # mock the dependencies
    mock_file_translator = mocker.MagicMock(
        side_effect=InvalidImageFileError("Bad file")
    )
    sample_user_id = uuid.uuid4()
    mock_db_session = AsyncMock(spec=AsyncSession)
    # do not need to mock the other dependencies as the function should fail early
    # create mock input data for the service function
    mock_file = mocker.MagicMock(spec=UploadFile)
    # mock the async read method
    mocker.patch.object(
        mock_file, "read", return_value=b"this_is_not_a_valid_image_file"
    )
    # inputs for process_and_save_image
    rotate_args = RotateArguments(processing="rotate", angle=100)
    validated_data = UploadRequestBody(arguments=rotate_args)
    # call the service with injected dependencies
    with pytest.raises(InvalidImageFileError):
        await process_and_save_image(
            file=mock_file,
            validated_data=validated_data,
            file_translator=mock_file_translator,
            db_session=mock_db_session,
            user_id=sample_user_id,
        )


async def test_process_and_save_image_raises_error_on_write_failure(mocker):
    """
    GIVEN a valid image file
    AND a valid upload request body
    AND the file_writer is mocked to raise a write failure
    WHEN the process_and_save_image service is called
    THEN an InvalidImageFileError is raised
    """
    # mock the dependencies
    mock_file_translator = mocker.MagicMock(return_value="numpy_array_data")
    mock_file_writer = mocker.MagicMock(side_effect=OSError("Disk full"))
    mock_db_session = mocker.MagicMock(spec=AsyncSession)
    sample_user_id = uuid.uuid4()
    # do not need to mock the other dependencies as the function should fail early
    # create mock input data for the service function
    mock_file = mocker.MagicMock(spec=UploadFile)
    mock_file.filename = "some_image_data.png"
    # mock the async read method
    mocker.patch.object(
        mock_file, "read", return_value=b"this_is_not_a_valid_image_file"
    )
    # inputs for process_and_save_image
    rotate_args = RotateArguments(processing="rotate", angle=100)
    validated_data = UploadRequestBody(arguments=rotate_args)
    # call the service with injected dependencies
    with pytest.raises(OSError):
        await process_and_save_image(
            file=mock_file,
            validated_data=validated_data,
            file_translator=mock_file_translator,
            file_writer=mock_file_writer,
            db_session=mock_db_session,
            user_id=sample_user_id,
        )
