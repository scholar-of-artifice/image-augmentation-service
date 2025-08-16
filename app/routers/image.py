import json
from fastapi import APIRouter, Form, UploadFile
from app.models.image_api.upload import UploadRequestBody
from pydantic import ValidationError
from app.internal.augmentations import shift, rotate
from app.internal.file_handling import translate_file_to_numpy_array, write_numpy_array_to_image_file


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
        # process image based on requested algorithm
        new_img_data = img_data
        file_path = ''
        if validated_data.arguments.processing == "shift":
            new_img_data = shift(image_data=img_data,
                                 direction=validated_data.arguments.direction,
                                 distance=validated_data.arguments.distance)
        elif validated_data.arguments.processing == "rotate":
            new_img_data = rotate(image_data=img_data,
                                  amount=validated_data.arguments.amount)
        file_path = write_numpy_array_to_image_file(data=new_img_data,
                                                    file_name='i_hope_this_works')
        # tell me where you put the file?
        return {
            "output_file_path": file_path,
            "body": body
        }
    except json.JSONDecodeError:
        # this should only happen when json.loads has an issue
        return {"error": "Invalid JSON format in the 'body' field"}
    except ValidationError as e:
        # this should happen when any validation fails
        return {"error": str(e)}
