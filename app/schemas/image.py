import uuid
from typing import Annotated, Literal

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

class FlipArguments(BaseModel):
    """
        A data model for specifying a 'flip' operation.

        This model is used to define the parameters for flipping an image.

        Attributes:
            processing (Literal["flip"]): The name of the operation. This field is fixed.
            axis (string): The direction of the flip.
    """
    # enforce specific value for processing field
    processing: Literal["flip"]
    # enforce the possible values
    axis: Literal["x"] | Literal["y"]

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


class SaltNoiseArguments(BaseModel):
    """
        A data model for specifying a 'salt_noise' operation.

        This model is used to define the parameters for making a noisey image.

        Attributes:
            processing (Literal["salt_noise"]): The type of operation. This field is fixed.
            amount (float): The ratio of pixels to overwrite.
    """
    # enforce specific value for processing field
    processing: Literal["salt_noise"]
    # enforce positive integer... 0 is no change
    amount: Annotated[float, Field(strict=True, gt=0, lt=1)]


class PepperNoiseArguments(BaseModel):
    """
        A data model for specifying a 'pepper_noise' operation.

        This model is used to define the parameters for applying noise to the image.

        Attributes:
            processing (Literal["pepper_noise"]): The type of operation. This field is fixed.
            amount (float): The ratio of pixels to overwrite.
    """
    # enforce specific value for processing field
    processing: Literal["pepper_noise"]
    # enforce positive integer... 0 is no change
    amount: Annotated[float, Field(strict=True, gt=0, lt=1)]

# TODO: deprecate
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


class AugmentationRequestBody(BaseModel):
    """
    This is the request body for:
        /image-api/augment/...
    """
    arguments: Annotated[
        ShiftArguments | RotateArguments | FlipArguments | RainbowNoiseArguments,
        Field(
            json_schema_extra={
                "descriminator": "processing"
            }
        )
    ]

# --- Service Layer Responses ---

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
        AugmentationRequestBody,
        Field(
            description="The way the image was requested to be augmented."
        )
    ]
