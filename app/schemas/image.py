from typing import Annotated, Literal
import uuid
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


class RainbowNoiseArguments(BaseModel):
    """
        A data model for specifying a 'rainbow_noise' operation.

        This model is used to define the parameters for shifting an image.

        Attributes:
            processing (Literal["shift"]): The type of operation. This field is fixed.
            amount (int): The distance of the shift. Must be a positive integer and greater than 0.
    """
    # enforce specific value for processing field
    processing: Literal["rainbow_noise"]
    # enforce positive integer... 0 is no change
    amount: Annotated[float, Field(strict=True, gt=0, lt=1)]

# TODO: deprecate this
class UploadRequestBody(BaseModel):
    """
    This is the request body for:
        /image-api/upload
    """
    arguments: Annotated[
        ShiftArguments | RotateArguments | RainbowNoiseArguments,
        Field(
            json_schema_extra={
                "descriminator": "processing"
            }
        )
    ]

# --- models for caputring the response from endpoints ---

class ResponseUploadImage(BaseModel):
    """
    This is the response body for:
    ```
    /image-api/upload/
    ```
    """
    unprocessed_image_id: Annotated[
        uuid.UUID,
        Field(
            description="The ID of the unprocessed image."
                        "\nUse this to:"
                        "\n- download the image"
                        "\n- make an augmentation of this specific image"
        )
    ]
    unprocessed_image_filename: Annotated[
        str,
        Field(
            description="The filename of the unprocessed image."
        )
    ]

class ResponseAugmentImage(BaseModel):
    """
    This is the response body for:
    ```
    /image-api/augment/{unprocessed_image_id}/
    ```
    """
    unprocessed_image_id: Annotated[
        uuid.UUID,
        Field(
            description="The ID of the unprocessed image."
                        "\nThis is the parent image of this augmentation."
        )
    ]
    processed_image_id: Annotated[
        uuid.UUID,
        Field(
            description="The ID of the processed image."
                        "\nUse this to:"
                        "\n- download the image"
        )
    ]
    processed_image_filename: Annotated[
        str,
        Field(
            description="The filename of the processed image."
        )
    ]
    request_body: Annotated[
        UploadRequestBody,
        Field(
            description="The way the image was requested to be augmented."
        )
    ]


# --- Models for capturing responses from Service Layer functions --- #

class ResponseWriteUnprocessedImageToStorage(BaseModel):
    """
    Response body for service layer:
        write_unprocessed_image_to_storage
    """
    user_id: Annotated[
        uuid.UUID,
        Field(description="The ID of the user that owns the image.")
    ]
    storage_filename: Annotated[
        str,
        Field(description="The filename of the unprocessed image.")
    ]
    image_location: Annotated[
        str,
        Field(description="The location of the unprocessed image.")
    ]
