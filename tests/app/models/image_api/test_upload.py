import pytest
from pydantic import ValidationError
from app.models.image_api.upload import ShiftArguments, RotateArguments, UploadRequestBody

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
        data = {
            "processing": "rotate",
            "angle": v
        }
        assert RotateArguments(**data).angle == v


def test_RotateArguments_shift_is_an_invalid_processing_type():
    """
    GIVEN an invalid processing_type
    WHEN a RotateArguments is created
    THEN it should raise an error
    """
    data = {
        "processing": "shift",
        "angle": 42
    }
    with pytest.raises(ValidationError):
        RotateArguments(**data)


def test_RotateArguments_negative_number_is_invalid_angle():
    """
    GIVEN an invalid angle of negative degrees
    WHEN a RotateArguments is created
    THEN it should raise an error
    """
    data = {
        "processing": "rotate",
        "angle": -42
    }
    with pytest.raises(ValidationError):
        RotateArguments(**data)


def test_RotateArguments_0_is_invalid_angle():
    """
    GIVEN an invalid angle of 0 degrees
    WHEN a RotateArguments is created
    THEN it should raise an error
    """
    data = {
        "processing": "rotate",
        "angle": 0
    }
    with pytest.raises(ValidationError):
        RotateArguments(**data)


def test_RotateArguments_360_is_invalid_angle():
    """
    GIVEN an invalid angle of 360 degrees
    WHEN a RotateArguments is created
    THEN it should raise an error
    """
    data = {
        "processing": "rotate",
        "angle": 360
    }
    with pytest.raises(ValidationError):
        RotateArguments(**data)

# --- UploadRequestBody ---


def test_UploadRequestBody_is_valid_when_arguments_are_for_rotate():
    """
        GIVEN a valid dictionary for rotate
        WHEN an UploadRequestBody is constructed
        THEN the expected data is stored
    """
    # a valid dictionary representing the request body
    data = {
        "arguments": {
            "processing": "rotate",
            "angle": 42
        }
    }
    # the UploadRequestBody is constructed from the dictionary
    result = UploadRequestBody(**data)
    # the model contains the correct data and types
    assert isinstance(result, UploadRequestBody)
    assert isinstance(result.arguments, RotateArguments)
    assert result.arguments.processing == "rotate"
    assert result.arguments.angle == 42