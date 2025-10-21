import uuid

import pytest
from pydantic import ValidationError

from app.schemas.image import (
    BrightenArguments,
    ChannelSwapArguments,
    CutoutArguments,
    DarkenArguments,
    EdgeFilterArguments,
    FlipArguments,
    GaussianBlurArguments,
    InvertArguments,
    MinFilterArguments,
    MuteChannelArguments,
    RotateArguments,
    ShiftArguments,
    TintArguments,
    UniformBlurArguments,
    ZoomArguments,
    AugmentationRequestBody,
    ResponseUploadImage
)

# --- BrightenArguments ---

def test_BrightenArguments_amount_of_value_0_is_valid():
    data = {
        "processing": "brighten",
        "amount": 100
    }
    brighten_args = BrightenArguments(**data)
    assert brighten_args.processing == "brighten"
    assert brighten_args.amount == 100

def test_BrightenArguments_amount_of_negative_value_is_not_valid():
    data = {
        "processing": "brighten",
        "amount": -1
    }
    with pytest.raises(ValidationError):
        BrightenArguments(**data)

# --- ShiftArguments ---


def test_ShiftArguments_up_is_a_valid_direction():
    data = {
        "processing": "shift",
        "direction": "up",
        "distance": 42,
    }
    shift_args = ShiftArguments(**data)
    assert shift_args.processing == "shift"
    assert shift_args.direction == "up"
    assert shift_args.distance == 42


def test_ShiftArguments_down_is_a_valid_direction():
    data = {
        "processing": "shift",
        "direction": "down",
        "distance": 42,
    }
    shift_args = ShiftArguments(**data)
    assert shift_args.processing == "shift"
    assert shift_args.direction == "down"
    assert shift_args.distance == 42


def test_ShiftArguments_left_is_a_valid_direction():
    data = {
        "processing": "shift",
        "direction": "left",
        "distance": 42,
    }
    shift_args = ShiftArguments(**data)
    assert shift_args.processing == "shift"
    assert shift_args.direction == "left"
    assert shift_args.distance == 42


def test_ShiftArguments_right_is_a_valid_direction():
    data = {
        "processing": "shift",
        "direction": "right",
        "distance": 42,
    }
    shift_args = ShiftArguments(**data)
    assert shift_args.processing == "shift"
    assert shift_args.direction == "right"
    assert shift_args.distance == 42


def test_ShiftArguments_mixed_case_right_is_an_invalid_direction():
    data = {
        "processing": "shift",
        "direction": "RiGHt",
        "distance": 42,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_rotate_is_an_invalid_processing_type():
    data = {
        "processing": "rotate",
        "direction": "right",
        "distance": 42,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_asdf_is_an_invalid_direction():
    data = {
        "processing": "shift",
        "direction": "asdf",
        "distance": 42,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_diagonal_is_an_invalid_direction():
    data = {
        "processing": "shift",
        "direction": "diagonal",
        "distance": 42,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_blank_string_is_an_invalid_direction():
    data = {
        "processing": "shift",
        "direction": "",
        "distance": 42,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_None_is_an_invalid_direction():
    data = {
        "processing": "shift",
        "direction": None,
        "distance": 42,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_None_is_an_invalid_distance():
    data = {
        "processing": "shift",
        "direction": "up",
        "distance": None,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_string_number_is_an_invalid_distance():
    data = {
        "processing": "shift",
        "direction": "up",
        "distance": "42",
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_0_is_an_invalid_distance():
    data = {
        "processing": "shift",
        "direction": "up",
        "distance": 0,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_negative_value_is_an_invalid_distance():
    data = {
        "processing": "shift",
        "direction": "up",
        "distance": -123,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_has_docstring():
    """
    GIVEN a type ShiftArguments
    WHEN ShiftArguments exists
    THEN it should have a docstring
    """
    assert ShiftArguments.__doc__ is not None
    assert "A data model for specifying a 'shift' operation." in ShiftArguments.__doc__


# --- RotateArguments ---


def test_RotateArguments_values_between_1_and_359_are_valid_angle():
    """
    GIVEN a valid angle
    AND a RotateArguments is created
    WHEN RotateArguments.angle is called
    THEN it should return the angle specified
    """
    valid_angle = list(range(1, 360))
    for v in valid_angle:
        data = {"processing": "rotate", "angle": v}
        assert RotateArguments(**data).angle == v


def test_RotateArguments_shift_is_an_invalid_processing_type():
    """
    GIVEN an invalid processing_type
    WHEN a RotateArguments is created
    THEN it should raise an error
    """
    data = {"processing": "shift", "angle": 42}
    with pytest.raises(ValidationError):
        RotateArguments(**data)


def test_RotateArguments_negative_number_is_invalid_angle():
    """
    GIVEN an invalid angle of negative degrees
    WHEN a RotateArguments is created
    THEN it should raise an error
    """
    data = {"processing": "rotate", "angle": -42}
    with pytest.raises(ValidationError):
        RotateArguments(**data)


def test_RotateArguments_0_is_invalid_angle():
    """
    GIVEN an invalid angle of 0 degrees
    WHEN a RotateArguments is created
    THEN it should raise an error
    """
    data = {"processing": "rotate", "angle": 0}
    with pytest.raises(ValidationError):
        RotateArguments(**data)


def test_RotateArguments_360_is_invalid_angle():
    """
    GIVEN an invalid angle of 360 degrees
    WHEN a RotateArguments is created
    THEN it should raise an error
    """
    data = {"processing": "rotate", "angle": 360}
    with pytest.raises(ValidationError):
        RotateArguments(**data)


# --- AugmentationRequestBody ---


def test_AugmentationRequestBody_is_valid_when_arguments_are_for_shift():
    """
    GIVEN a valid dictionary for shift
    WHEN an AugmentationRequestBody is constructed
    THEN the expected data is stored
    """
    # a valid dictionary representing the request body
    data = {"arguments": {"processing": "shift", "direction": "up", "distance": 42}}
    # the AugmentationRequestBody is constructed from the dictionary
    result = AugmentationRequestBody(**data)
    # the model contains the correct data and types
    assert isinstance(result, AugmentationRequestBody)
    assert isinstance(result.arguments, ShiftArguments)
    assert result.arguments.processing == "shift"
    assert result.arguments.direction == "up"
    assert result.arguments.distance == 42


def test_AugmentationRequestBody_is_valid_when_arguments_are_for_rotate():
    """
    GIVEN a valid dictionary for rotate
    WHEN an AugmentationRequestBody is constructed
    THEN the expected data is stored
    """
    # a valid dictionary representing the request body
    data = {"arguments": {"processing": "rotate", "angle": 42}}
    # the AugmentationRequestBody is constructed from the dictionary
    result = AugmentationRequestBody(**data)
    # the model contains the correct data and types
    assert isinstance(result, AugmentationRequestBody)
    assert isinstance(result.arguments, RotateArguments)
    assert result.arguments.processing == "rotate"
    assert result.arguments.angle == 42


def test_AugmentationRequestBody_is_invalid_when_arguments_not_part_of_any_model():
    """
    GIVEN an invalid dictionary for any argument is created
    WHEN an AugmentationRequestBody is constructed
    THEN an exception is raised
    """
    data = {"arguments": {"what?": "goblins", "there->": 30.235}}
    with pytest.raises(ValidationError):
        AugmentationRequestBody(**data)


# --- ResponseUploadImage ---

def test_ResponseUploadImage_is_valid():
    """
    GIVEN a valid set of inputs
    WHEN an ResponseUploadImage object is constructed
    THEN the expected data is stored correctly
    """
    # create valid set of parameters for ImageProcessResponse
    test_unprocessed_id = uuid.uuid4()
    test_unprocessed_filename = str(uuid.uuid4()) + '.png'
    # construct the ResponseUploadImage object
    response = ResponseUploadImage(
        unprocessed_image_id=test_unprocessed_id,
        unprocessed_image_filename=test_unprocessed_filename
    )
    # check that the data is stored correctly
    assert response.unprocessed_image_id == test_unprocessed_id
    assert response.unprocessed_image_filename == test_unprocessed_filename
    assert isinstance(response.unprocessed_image_id, uuid.UUID)
    assert isinstance(response.unprocessed_image_filename, str)


def test_ResponseUploadImage_is_not_valid_when_image_id_is_not_uuid():
    """
    GIVEN a valid set of inputs
    WHEN an ResponseUploadImage object is constructed
    THEN the expected data is stored correctly
    """
    # create valid set of parameters for ImageProcessResponse
    test_unprocessed_id = 'not a uuid at all'
    test_unprocessed_filename = str(uuid.uuid4()) + '.png'
    # check that the data is not stored with error
    with pytest.raises(ValidationError):
        ResponseUploadImage(
            unprocessed_image_id=test_unprocessed_id,
            unprocessed_image_filename=test_unprocessed_filename
        )

