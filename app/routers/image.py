
from fastapi import APIRouter
from app.models.image_api.upload import UploadRequestBody

router = APIRouter()


@router.post("/upload/")
async def upload(body: UploadRequestBody):
    # TODO: this is a POST request which will allow a user to upload an image
    print('hello from upload')
    print(body)
    return {"filename": 'file.filename', "message": "Image processed successfully.", "your_choice": "your choice was " + body.processing + "."}
