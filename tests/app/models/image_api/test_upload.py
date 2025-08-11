import pytest
from pydantic import ValidationError
from app.models.image_api.upload import ProcessingEnum, ShiftArguments


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
