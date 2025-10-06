import pytest

from app.exceptions.directory_manager import (
    ImageDirectoryNotFound,
    UserDirectoryNotFound,
)


def fake_UserDirectoryNotFound_function():
    if True:
        raise UserDirectoryNotFound(
            "The user directory is not found!"
        )


def fake_ImageDirectoryNotFound_function():
    if True:
        raise ImageDirectoryNotFound(
            "The user directory is not found!"
        )

def test_UserDirectoryNotFound_is_raised():
    """
    GIVEN an UserDirectoryNotFound exception
    WHEN fake_UserDirectoryNotFound_function is called
    THEN it should raise UserDirectoryNotFound
    """
    with pytest.raises(UserDirectoryNotFound):
        fake_UserDirectoryNotFound_function()


def test_ImageDirectoryNotFound_is_raised():
    """
    GIVEN an ImageDirectoryNotFound exception
    WHEN fake_ImageDirectoryNotFound_function is called
    THEN it should raise ImageDirectoryNotFound
    """
    with pytest.raises(ImageDirectoryNotFound):
        fake_ImageDirectoryNotFound_function()
