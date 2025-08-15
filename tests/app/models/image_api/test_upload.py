import pytest
from pydantic import ValidationError
from app.models.image_api.upload import ShiftArguments, RotateArguments, UploadRequestBody


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


def test_RotateArguments_values_between_1_and_359_are_valid_amount():
    valid_amount = list(range(1, 360))
    for v in valid_amount:
        data = {
            "processing": "rotate",
            "amount": v
        }
        assert RotateArguments(**data).amount == v


def test_RotateArguments_shift_is_an_invalid_processing_type():
    data = {
        "processing": "shift",
        "amount": 42
    }
    with pytest.raises(ValidationError):
        RotateArguments(**data)


def test_RotateArguments_negative_number_is_invalid_amount():
    data = {
        "processing": "rotate",
        "amount": -42
    }
    with pytest.raises(ValidationError):
        RotateArguments(**data)


def test_RotateArguments_0_is_invalid_amount():
    data = {
        "processing": "rotate",
        "amount": 0
    }
    with pytest.raises(ValidationError):
        RotateArguments(**data)


def test_RotateArguments_360_is_invalid_amount():
    data = {
        "processing": "rotate",
        "amount": 360
    }
    with pytest.raises(ValidationError):
        RotateArguments(**data)
