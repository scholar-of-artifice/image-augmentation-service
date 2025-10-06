import pytest

from app.exceptions.directory_manager import (
    ImageDirectoryNotFound,
    UserDirectoryAlreadyExists,
    UserDirectoryNotFound,
)

# --- ImageDirectoryNotFound ---

def fake_ImageDirectoryNotFound_function():
    raise ImageDirectoryNotFound(
        "The image directory /foo/ is not found!"
    )

# --- UserDirectoryAlreadyExists ---

def fake_UserDirectoryAlreadyExists_function():
    raise UserDirectoryAlreadyExists(
        "The user directory /foo/ already exists."
    )

# --- UserDirectoryNotFound ---

def fake_UserDirectoryNotFound_function():
    raise UserDirectoryNotFound(
        "The user directory /foo/ is not found!"
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


def test_UserDirectoryAlreadyExists_is_raised():
    """
    GIVEN a UserDirectoryAlreadyExists exception
    WHEN fake_UserDirectoryAlreadyExists_function is called
    THEN it should raise UserDirectoryAlreadyExists
    """
    with pytest.raises(UserDirectoryAlreadyExists):
        fake_UserDirectoryAlreadyExists_function()
