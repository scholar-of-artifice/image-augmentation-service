import json
from fastapi import (APIRouter, Form, UploadFile, HTTPException, status)
from app.models.image_api.upload import UploadRequestBody
from pydantic import ValidationError
from app.internal.augmentations import shift, rotate
from app.internal.file_handling import (translate_file_to_numpy_array, write_numpy_array_to_image_file, create_file_name)

router = APIRouter()


@router.post("/upload/")
async def upload(file: UploadFile, body: str = Form(...)):
    """
        Request processing of an image file.

        Arguments:
            file {UploadFile} -- The image file to be processed.
            body {str} -- A JSON string containing the body of the request.
    """
    try:
        # get the json data
        json_data = json.loads(body)
        # validate the incoming data against the pydantic model.
        validated_data = UploadRequestBody(**json_data)
        # asynchronously read the contents of the uploaded file as bytes
        image_content = await file.read()
        # convert the raw image bytes into a numpy array
        img_data = translate_file_to_numpy_array(image_content)
        # save a copy of the original unprocessed image to the 'unprocessed_image_data' volume.
        original_stored_file_path = write_numpy_array_to_image_file(data=img_data,
                                        file_name=file.filename,
                                        destination_volume='unprocessed_image_data')
        # initialize a new variables for the processed image data
        new_img_data = img_data
        # check the processing argument from the request to determine which action to take
        if validated_data.arguments.processing == "shift":
            # apply shift
            new_img_data = shift(image_data=img_data,
                                 direction=validated_data.arguments.direction,
                                 distance=validated_data.arguments.distance)
        elif validated_data.arguments.processing == "rotate":
            # appy rotate
            new_img_data = rotate(image_data=img_data,
                                  angle=validated_data.arguments.angle)

        # save a the processed image to the 'processed_image_data' volume.
        new_stored_file_path = write_numpy_array_to_image_file(data=new_img_data,
                                                    file_name=create_file_name(),
                                                    destination_volume='processed_image_data')
        # return the file paths for both the original and unprocessed images
        return {
            "original_stored_file_path": original_stored_file_path,
            "new_stored_file_path": new_stored_file_path,
            "body": body
        }
    except json.JSONDecodeError:
        # this should only happen when json.loads has an issue
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON format in the `body` field."
        )
    except ValidationError as e:
        error_message = []
        for error in e.errors():
            field = " -> ".join(map(str, error['loc']))
            message = error['msg']
            error_message.append(f"Error in {field}: {message}")
        # this should happen when any validation fails
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="".join(error_message)
        )
