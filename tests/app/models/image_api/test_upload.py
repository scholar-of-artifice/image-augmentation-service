import pytest

from app.models.image_api.upload import ProcessingEnum


def test_ProcessingEnum_has_correct_contents():
    assert ProcessingEnum.shift == "shift"
    assert ProcessingEnum.rotate == "rotate"
