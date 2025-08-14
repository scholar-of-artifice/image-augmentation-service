import json
from fastapi import APIRouter, Form, UploadFile
from app.models.image_api.upload import UploadRequestBody
from pydantic import ValidationError


router = APIRouter()


@router.post("/upload/")
async def upload(body: str = Form(...), file: UploadFile = Form(...)):
    print('hello from upload')
    print(body)
    print(file.filename)
    # TODO: validate form data within this request
    try:
        json_data = json.loads(body)
        validated_data = UploadRequestBody(**json_data)
        arguments = validated_data.arguments
        if arguments.processing == "shift":
            # TODO: apply shift to image
            print("shift")
        elif arguments.processing == "rotate":
            # TODO: apply rotate to image
            print("rotate")
        return {
            "filename": file.filename,
            "message": "Image processed successfully."
        }
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the 'body' field"}
    except ValidationError as e:
        return {"error": str(e)}
    return {
        "filename": file.filename,
        "message": "Image not processed."
    }
