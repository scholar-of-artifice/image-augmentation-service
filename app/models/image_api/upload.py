from enum import Enum
from typing import Annotated
from pydantic import BaseModel, Field
from pydantic.types import StringConstraints

# TODO: there will be more functions listed here
# TODO: handle parameters for each function


class ProcessingEnum(str, Enum):
    shift = "shift"
    rotate = "rotate"


class ShiftArguments(BaseModel):
    # enforce specific string constraints
    direction: Annotated[str, StringConstraints(
        min_length=2,
        max_length=5,
        strip_whitespace=True,
        strict=True,
        to_lower=True,
        pattern="^(up|down|left|right)$")]
    # enforce positive integer... 0 is no change
    distance: Annotated[int, Field(strict=True, gt=0)]


class RotateArguments(BaseModel):
    # enforce integer range
    amount: Annotated[int, Field(strict=True, gt=0, lt=360)]


class UploadRequestBody(BaseModel):
    """
    This is the request body for:
        /image-api/upload
    """
    processing: ProcessingEnum
    arguments: ShiftArguments
