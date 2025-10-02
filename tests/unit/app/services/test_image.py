import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.file_handling import InvalidImageFileError
from app.schemas.image import RotateArguments, ShiftArguments, UploadRequestBody, ResponseUploadImage
from app.schemas.transactions_db import UnprocessedImage, User
from app.services.image import get_unprocessed_image_by_id, process_and_save_image, save_unprocessed_image, create_UnprocessedImage_entry

pytestmark = pytest.mark.asyncio

async def NO_test_save_unprocessed_image_succeeds(mocker):
    """
    GIVEN an unprocessed image
    WHEN the `save_unprocessed_image` method is called
    THEN it should succeed
    """
    # mock the injected dependencies
    mock_file_translator = mocker.patch(
        "app.services.image.translate_file_to_numpy_array",
        return_value="numpy_array_data"
    )
    mock_file_writer = mocker.patch(
        "app.services.image.write_numpy_array_to_image_file"
    )
    mock_filename_creator = mocker.patch(
        "app.services.image.create_file_name",
        return_value="new_filename.png"
    )
    # create mock objects for the function arguments
    test_user_id = uuid.uuid4()
    test_file_content = b"fake image data"
    test_original_filename = "test_original_filename.png"
    # mock the UploadFile object
    mock_upload_file = MagicMock(spec=UploadFile)
    mock_upload_file.filename = test_original_filename
    mock_upload_file.read = AsyncMock(return_value=test_file_content)
    # mock the async session
    mock_db_session = AsyncMock()
    # simulate db_refresh
    new_image_id = uuid.uuid4()
    def simulate_db_refresh(record_to_refresh):
        record_to_refresh.id = new_image_id
    mock_db_session.refresh.side_effect = simulate_db_refresh
    # call the function
    result = await save_unprocessed_image(
        file=mock_upload_file,
        user_id=test_user_id,
        db_session=mock_db_session,
        file_translator=mock_file_translator,
        file_writer=mock_file_writer,
        filename_creator=mock_filename_creator,
    )
    # check the result
    assert isinstance(result, ResponseUploadImage)
    assert result.unprocessed_image_id == new_image_id
    assert result.unprocessed_image_filename == "new_filename.png"


async def test_save_unprocessed_image_fails_when_original_filename_missing(mocker):
    """
    GIVEN an unprocessed image
    AND the image has no filename
    WHEN the `save_unprocessed_image` method is called
    THEN it should fail
    """
    # mock the injected dependencies
    mock_file_translator = mocker.patch(
        "app.services.image.translate_file_to_numpy_array",
        return_value="numpy_array_data"
    )
    mock_file_writer = mocker.patch(
        "app.services.image.write_numpy_array_to_image_file"
    )
    mock_filename_creator = mocker.patch(
        "app.services.image.create_file_name",
        return_value="new_filename.png"
    )
    # create mock objects for the function arguments
    test_user_id = uuid.uuid4()
    test_file_content = b"fake image data"
    test_original_filename = ""
    # mock the UploadFile object
    mock_upload_file = MagicMock(spec=UploadFile)
    mock_upload_file.filename = test_original_filename
    mock_upload_file.read = AsyncMock(return_value=test_file_content)
    # mock the async session
    mock_db_session = AsyncMock()
    # simulate db_refresh
    new_image_id = uuid.uuid4()
    def simulate_db_refresh(record_to_refresh):
        record_to_refresh.id = new_image_id
    mock_db_session.refresh.side_effect = simulate_db_refresh
    with pytest.raises(HTTPException) as e:
        # call the function
        result = await save_unprocessed_image(
            file=mock_upload_file,
            user_id=test_user_id,
            db_session=mock_db_session,
            file_translator=mock_file_translator,
            file_writer=mock_file_writer,
            filename_creator=mock_filename_creator,
        )
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST
    assert e.value.detail == "No filename provided."
    # check no side effects occurred
    mock_file_translator.assert_not_called()
    mock_db_session.add.assert_not_called()


async def NO_test_process_and_save_image_with_shift_arguments_succeeds(mocker):
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
    assert isinstance(result.body, UploadRequestBody)
    assert isinstance(result.unprocessed_image_id, uuid.UUID)
    assert isinstance(result.processed_image_id, uuid.UUID)
    assert isinstance(result.processing_job_id, uuid.UUID)


async def NO_test_process_and_save_image_with_rotate_arguments_succeeds(mocker):
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
    assert isinstance(result.body, UploadRequestBody)
    assert isinstance(result.unprocessed_image_id, uuid.UUID)
    assert isinstance(result.processed_image_id, uuid.UUID)
    assert isinstance(result.processing_job_id, uuid.UUID)


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
    mock_db_session = AsyncMock(spec=AsyncSession)
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


async def test_get_unprocessed_image_by_id_is_success_when_image_exists(mocker):
    """
    GIVEN an unprocessed_image exists with example_image_id
    AND the example_image_id is given
    WHEN the get_unprocessed_image_by_id service is called
    THEN the correct image date is returned
    """
    test_image_id = uuid.uuid4()
    test_user_id = uuid.uuid4()
    mock_user_entry = User(
        id=test_user_id,
        external_id='some_external_id',
    )
    mock_image_entry = UnprocessedImage(
        id=test_image_id,
        user_id=test_user_id,
        original_filename="some_image_data.png",
        storage_filename=f"{str(uuid.uuid4())}.png",
    )
    mock_db_session = AsyncMock(spec=AsyncSession)
    mock_user_result = MagicMock()
    mock_user_result.scalar_one_or_none.return_value = mock_user_entry
    mock_image_result = MagicMock()
    mock_image_result.scalar_one_or_none.return_value = mock_image_entry
    mock_db_session.execute.side_effect = [mock_user_result, mock_image_result]

    result = await get_unprocessed_image_by_id(
        unprocessed_image_id=test_image_id,
        db_session=mock_db_session,
        user_id=test_user_id
    )
    mock_db_session.execute.call_count == 2
    assert result == mock_image_entry
    assert result.id == test_image_id
    assert result.user_id == test_user_id
    assert result.original_filename == "some_image_data.png"


async def test_get_unprocessed_image_by_id_is_not_found_when_image_does_not_exist(mocker):
    """
    GIVEN an unprocessed_image exists with example_image_id
    AND a different example_image_id is given
    WHEN the test_get_unprocessed_image_by_id_is_success_when_image_exists service is called
    THEN a 404 is raised
    """
    test_image_id = uuid.uuid4()
    test_user_id = uuid.uuid4()
    mock_db_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_session.execute.return_value = mock_result
    with pytest.raises(HTTPException) as http_exception:
        await get_unprocessed_image_by_id(
            unprocessed_image_id=test_image_id,
            db_session=mock_db_session,
            user_id=test_user_id
        )
    mock_db_session.execute.assert_called_once()
    assert http_exception.value.status_code == 404


async def test_get_unprocessed_image_by_id_is_not_found_when_a_different_user_requests_an_image_that_they_do_not_own(mocker):
    """
    GIVEN an unprocessed_image exists with example_image_id
    AND a different user_id makes the request
    WHEN the test_get_unprocessed_image_by_id_is_success_when_image_exists service is called
    THEN a 404 is raised
    """
    test_image_id = uuid.uuid4()
    test_user_id = uuid.uuid4()
    mock_db_session = AsyncMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_session.execute.return_value = mock_result
    with pytest.raises(HTTPException) as http_exception:
        await get_unprocessed_image_by_id(
            unprocessed_image_id=test_image_id,
            db_session=mock_db_session,
            user_id=test_user_id
        )
    mock_db_session.execute.assert_called_once()
    assert http_exception.value.status_code == 404

# --- overhaul services layer APIs ---

async def test_create_UnprocessedImage_entry_is_successful(mocker):
    """
    GIVEN a user_id
    AND an original_filename
    AND a unique storage filename
    WHEN create_UnprocessedImage_entry is called
    THEN a new UnprocessedImage entry is created
    AND the entry is added to the database session
    """
    test_user_id = uuid.uuid4()
    test_original_filename = "some_original_filename.png"
    test_storage_filename = f"{str(uuid.uuid4())}.png"
    mock_db_session = AsyncMock(spec=AsyncSession)
    # call the function
    result = await create_UnprocessedImage_entry(
        user_id=test_user_id,
        original_filename=test_original_filename,
        unprocessed_storage_filename=test_storage_filename,
        db_session=mock_db_session
    )
    # check the conditions of the test are met
    mock_db_session.add.assert_called_once()
    mock_db_session.flush.assert_awaited_once()
    assert isinstance(result, UnprocessedImage)
    assert result.user_id == test_user_id
    assert result.original_filename == test_original_filename
    assert result.storage_filename == test_storage_filename
