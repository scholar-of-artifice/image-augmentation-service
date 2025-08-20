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
            file {UploadFile} -- Upload file
            body {str} -- Image body
        Returns:
            dict -- Image body
    """
    try:
        # get the json data
        json_data = json.loads(body)
        validated_data = UploadRequestBody(**json_data)
        # get image contents
        image_content = await file.read()
        img_data = translate_file_to_numpy_array(image_content)
        write_numpy_array_to_image_file(data=img_data,
                                        file_name=file.filename,
                                        destination_volume='unprocessed_image_data')
        # process image based on requested algorithm
        new_img_data = img_data
        if validated_data.arguments.processing == "shift":
            new_img_data = shift(image_data=img_data,
                                 direction=validated_data.arguments.direction,
                                 distance=validated_data.arguments.distance)
        elif validated_data.arguments.processing == "rotate":
            new_img_data = rotate(image_data=img_data,
                                  angle=validated_data.arguments.angle)
        file_path = write_numpy_array_to_image_file(data=new_img_data,
                                                    file_name=create_file_name(),
                                                    destination_volume='processed_image_data')
        # tell me where you put the file?
        return {
            "output_file_path": file_path,
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
