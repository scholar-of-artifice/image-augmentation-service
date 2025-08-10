
from fastapi import APIRouter

router = APIRouter()


@router.post("/upload/")
async def upload():
    # TODO: this is a POST request which will allow a user to upload an image
    print('hello from upload')
    return {"filename": 'file.filename', "message": "Image processed successfully.", "your_choice": "your choice was " + "user_choice" + "."}
