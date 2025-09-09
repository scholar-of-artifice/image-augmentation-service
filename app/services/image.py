from app.schemas.image_api.upload import UploadRequestBody, ImageProcessResponse
from fastapi import UploadFile
from typing import Callable
from app.internal.file_handling import translate_file_to_numpy_array, write_numpy_array_to_image_file, create_file_name
from app.internal.augmentations import shift, rotate

async def process_and_save_image(
        file: UploadFile,
        validated_data: UploadRequestBody,
        # --- INJECTED DEPENDENCIES ---
        file_translator: Callable = translate_file_to_numpy_array,
        file_writer: Callable = write_numpy_array_to_image_file,
        filename_creator: Callable = create_file_name,
        shift_processor: Callable = shift,      # TODO: this is probably changing later
        rotate_processor: Callable = rotate,    # TODO: this is probably changing later
    ) -> ImageProcessResponse:
    """
        Handles the core logic of processing and saving an image.
    """
    # read and convert the image
    # asynchronously read the contents of the uploaded file as bytes
    image_content = await file.read()
    # convert the raw image bytes into a numpy array
    image_data = file_translator(image_content)
    # save a copy of the original unprocessed image to the 'unprocessed_image_data' volume.
    unprocessed_image_location = file_writer(
        data=image_data,
        file_name=file.filename,
        destination_volume='unprocessed_image_data'
    )
    # process the image
    # initialize a new variables for the processed image data
    new_img_data = image_data
    # check the processing argument from the request to determine which action to take
    if validated_data.arguments.processing == "shift":
        # apply shift
        new_img_data = shift_processor(
            image_data=image_data,
            direction=validated_data.arguments.direction,
            distance=validated_data.arguments.distance
        )
    elif validated_data.arguments.processing == "rotate":
        # appy rotate
        new_img_data = rotate_processor(
            image_data=image_data,
            angle=validated_data.arguments.angle
        )
    # save the processed image to the 'processed_image_data' volume.
    processed_image_location = file_writer(
        data=new_img_data,
        file_name=filename_creator(),
        destination_volume='processed_image_data'
    )
    # return an ImageProcessResponse
    return ImageProcessResponse(
        original_stored_file_path=unprocessed_image_location,
        new_stored_file_path=processed_image_location,
        body=validated_data
    )