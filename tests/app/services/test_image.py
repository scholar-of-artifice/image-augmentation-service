# Import your schemas and the service function
from app.models.image_api.upload import UploadRequestBody, ShiftArguments, RotateArguments
from app.services.image import process_and_save_image

