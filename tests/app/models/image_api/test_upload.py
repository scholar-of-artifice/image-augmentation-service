import pytest
from pydantic import ValidationError
from app.models.image_api.upload import ProcessingEnum, ShiftArguments, RotateArguments, UploadRequestBody


def test_ProcessingEnum_has_shift():
    assert ProcessingEnum.shift == "shift"


def test_ProcessingEnum_has_rotate():
    assert ProcessingEnum.rotate == "rotate"


def test_ShiftArguments_up_is_a_valid_direction():
    data = {
        "direction": "up",
        "distance": 42,
    }
    assert ShiftArguments(**data).direction == "up"
    assert ShiftArguments(**data).distance == 42


def test_ShiftArguments_down_is_a_valid_direction():
    data = {
        "direction": "down",
        "distance": 42,
    }
    assert ShiftArguments(**data).direction == "down"
    assert ShiftArguments(**data).distance == 42


def test_ShiftArguments_left_is_a_valid_direction():
    data = {
        "direction": "left",
        "distance": 42,
    }
    assert ShiftArguments(**data).direction == "left"
    assert ShiftArguments(**data).distance == 42


def test_ShiftArguments_right_is_a_valid_direction():
    data = {
        "direction": "right",
        "distance": 42,
    }
    assert ShiftArguments(**data).direction == "right"
    assert ShiftArguments(**data).distance == 42


def test_ShiftArguments_asdf_is_an_invalid_direction():
    data = {
        "direction": "asdf",
        "distance": 42,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_diagonal_is_an_invalid_direction():
    data = {
        "direction": "diagonal",
        "distance": 42,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_blank_string_is_an_invalid_direction():
    data = {
        "direction": "",
        "distance": 42,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_None_is_an_invalid_direction():
    data = {
        "direction": None,
        "distance": 42,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_0_is_an_invalid_distance():
    data = {
        "direction": "up",
        "distance": 0,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_negative_value_is_an_invalid_distance():
    data = {
        "direction": "up",
        "distance": -123,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_RotateArguments_values_between_1_and_359_are_valid_amount():
    valid_amount = list(range(1, 360))
    for v in valid_amount:
        data = {
            "amount": v
        }
        assert RotateArguments(**data).amount == v


def test_RotateArguments_invalid_arguments_raise_ValidationError():
    # TODO: comment this test
    data = {
        "amount": 0
    }
    with pytest.raises(ValidationError):
        RotateArguments(**data)

    data = {
        "amount": 360
    }
    with pytest.raises(ValidationError):
        RotateArguments(**data)


def test_UploadRequestBody_shift_with_ShiftArguments_is_valid():
    # TODO: comment this better
    data = {
        "processing": ProcessingEnum.shift,
        "arguments": ShiftArguments(direction="up", distance=10)
    }
    assert UploadRequestBody(**data).processing == "shift"
    assert UploadRequestBody(**data).arguments.direction == "up"
    assert UploadRequestBody(**data).arguments.distance == 10


def test_UploadRequestBody_rotate_with_RotateArguments_is_valid():
    # TODO: comment this better
    data = {
        "processing": ProcessingEnum.rotate,
        "arguments": RotateArguments(amount=10)
    }
    assert UploadRequestBody(**data).processing == "rotate"
    assert UploadRequestBody(**data).arguments.amount == 10


def test_UploadRequestBody_shift_with_RotateArguments_raise_ValidationError():
    # TODO: comment this better
    data = {
        "processing": ProcessingEnum.shift,
        "arguments": RotateArguments(amount=10)
    }
    with pytest.raises(ValidationError):
        UploadRequestBody(**data)


def test_UploadRequestBody_rotate_with_ShiftArguments_raise_ValidationError():
    # TODO: comment this better
    data = {
        "processing": ProcessingEnum.rotate,
        "arguments": ShiftArguments(direction="up", distance=10)
    }
    with pytest.raises(ValidationError):
        UploadRequestBody(**data)
