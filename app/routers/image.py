
from fastapi import APIRouter, Form, UploadFile
from app.models.image_api.upload import UploadRequestBody

router = APIRouter()


@router.post("/upload/")
async def upload(body: str = Form(...), file: UploadFile = Form(...)):
    print('hello from upload')
    # TODO: validate form data within this request
    print(body)
    print(file.filename)
    return {"filename": 'file.filename', "message": "Image processed successfully."}
