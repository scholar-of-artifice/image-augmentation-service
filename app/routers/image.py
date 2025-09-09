from fastapi import (APIRouter, Depends, UploadFile)
from app.schemas.image import UploadRequestBody, ImageProcessResponse
from app.dependency import get_body_as_model
from app.services.image import process_and_save_image

router = APIRouter()


@router.post(
    path="/upload/",
    response_model=ImageProcessResponse
)
async def upload(
        file: UploadFile,
        validated_data: UploadRequestBody = Depends(get_body_as_model)):
    """
        Request processing of an image file.

        Arguments:
            file {UploadFile} -- The image file to be processed.
            validated_data {UploadRequestBody} -- The parsed and validated request body.
    """
    return await process_and_save_image(file, validated_data)

