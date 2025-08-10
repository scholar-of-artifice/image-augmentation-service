from enum import Enum
from pydantic import BaseModel

# TODO: there will be more functions listed here
# TODO: handle parameters for each function


class ProcessingEnum(str, Enum):
    shift = "shift"
    rotate = "rotate"


class UploadRequestBody(BaseModel):
    """
    This is the request body for:
        /image-api/upload
    """
    processing: ProcessingEnum
