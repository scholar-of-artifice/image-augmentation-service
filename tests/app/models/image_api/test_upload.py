import pytest
from pydantic import ValidationError
from app.models.image_api.upload import ProcessingEnum, ShiftArguments, RotateArguments, UploadRequestBody


def test_ProcessingEnum_has_correct_contents():
    assert ProcessingEnum.shift == "shift"
    assert ProcessingEnum.rotate == "rotate"


def test_ShiftArguments_valid_arguments_are_allowed():
    # TODO: write better description and comments
    data = {
        "direction": "up",
        "distance": 13,
    }
    assert ShiftArguments(**data).direction == "up"
    assert ShiftArguments(**data).distance == 13

    data = {
        "direction": "down",
        "distance": 10,
    }
    assert ShiftArguments(**data).direction == "down"
    assert ShiftArguments(**data).distance == 10

    data = {
        "direction": "left",
        "distance": 2,
    }
    assert ShiftArguments(**data).direction == "left"
    assert ShiftArguments(**data).distance == 2

    data = {
        "direction": "right",
        "distance": 333,
    }
    assert ShiftArguments(**data).direction == "right"
    assert ShiftArguments(**data).distance == 333


def test_ShiftArguments_invalid_direction_raises_ValidationError():
    # TODO: comment this test
    data = {
        "direction": "asdf",
        "distance": 13,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)

    data = {
        "direction": "diagonal",
        "distance": 2,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_ShiftArguments_invalid_distance_raises_ValidationError():
    # TODO: comment this test
    data = {
        "direction": "up",
        "distance": 0,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)

    data = {
        "direction": "down",
        "distance": -123,
    }
    with pytest.raises(ValidationError):
        ShiftArguments(**data)


def test_RotateArguments_valid_arguments_are_allowed():
    # TODO: comment this test
    data = {
        "amount": 2
    }
    assert RotateArguments(**data).amount == 2

    data = {
        "amount": 82
    }
    assert RotateArguments(**data).amount == 82

    data = {
        "amount": 182
    }
    assert RotateArguments(**data).amount == 182

    data = {
        "amount": 359
    }
    assert RotateArguments(**data).amount == 359


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
