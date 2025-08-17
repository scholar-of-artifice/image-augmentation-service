from typing import Annotated, Union, Literal
from pydantic import BaseModel, Field
from pydantic.types import StringConstraints

"""
Models for: Inputs schema
endpoint: .../image-api/upload
"""

class ShiftArguments(BaseModel):
    """
        A data model for specifying a 'shift' operation.

        This model is used to define the parameters for shifting an image.

        Attributes:
            processing (Literal["shift"]): The type of operation. This field is fixed.
            direction (str): The direction of the shift. Must have a value of "up", "down", "left", or "right".
            distance (int): The distance of the shift. Must be a positive integer and greater than 0.
    """
    # enforce specific value for processing field
    processing: Literal["shift"]
    # enforce specific string constraints for direction
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
    """
        A data model for specifying a 'rotate' operation.

        This model is used to define the parameters for rotating an image.

        Attributes:
            processing (Literal["rotate"]): The name of the operation. This field is fixed.
            angle (int): The amount of rotation in degrees. Must be a postive integer between 1 and 359.
    """
    # enforce specific value for processing field
    processing: Literal["rotate"]
    # enforce integer range
    angle: Annotated[int, Field(strict=True, gt=0, lt=360)]


class UploadRequestBody(BaseModel):
    """
    This is the request body for:
        /image-api/upload
    """
    arguments: Annotated[Union[ShiftArguments,
                               RotateArguments], Field(json_schema_extra={"descriminator": "processing"})]


"""
Models for: Output schema
endpoint: .../image-api/upload
"""
