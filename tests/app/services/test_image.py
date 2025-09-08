from app.models.image_api.upload import UploadRequestBody, ShiftArguments, RotateArguments
from app.services.image import process_and_save_image

import pytest

pytestmark = pytest.mark.asyncio