from typing import Annotated, Union, Literal
from pydantic import BaseModel, Field
from pydantic.types import StringConstraints


class ShiftArguments(BaseModel):
    processing: Literal["shift"]
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
    processing: Literal["rotate"]
    # enforce integer range
    amount: Annotated[int, Field(strict=True, gt=0, lt=360)]


class UploadRequestBody(BaseModel):
    """
    This is the request body for:
        /image-api/upload
    """
    arguments: Annotated[Union[ShiftArguments,
                               RotateArguments], Field(json_schema_extra={"descriminator": "processing"})]
