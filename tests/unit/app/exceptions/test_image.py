import pytest

from app.exceptions.image import ImageNotFound


def fake_ImageNotFound_function():
    if True:
        raise ImageNotFound(
            "The image is not found!"
        )

def test_ImageNotFound_is_raised():
    """
    GIVEN an ImageNotFound exception
    WHEN fake_ImageNotFound_function is called
    THEN it should raise ImageNotFound
    """
    with pytest.raises(ImageNotFound):
        fake_ImageNotFound_function()
