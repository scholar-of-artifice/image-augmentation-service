from enum import Enum
from typing import Annotated, Union
from pydantic import BaseModel, Field, model_validator, ValidationError
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
    arguments: Union[ShiftArguments, RotateArguments]

    @model_validator(mode='before')
    def validate_arguments_match_processing(cls, data: dict) -> dict:
        # TODO: Comment and docstring
        processing, arguments = data.get("processing"), data.get("arguments")
        if not processing or not arguments:
            raise ValueError(
                "Both processing and arguments fields are required.")
        if processing == ProcessingEnum.shift:
            try:
                ShiftArguments.model_validate(arguments)
            except ValidationError as e:
                raise ValueError(f"Arguments for shift are invalid. {e}")
        if processing == ProcessingEnum.rotate:
            try:
                RotateArguments.model_validate(arguments)
            except ValidationError as e:
                raise ValueError(f"Arguments for rotate are invalid: {e}")

        return data
