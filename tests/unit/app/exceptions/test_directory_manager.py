import pytest

from app.exceptions.directory_manager import UserDirectoryNotFound


def fake_UserDirectoryNotFound_function():
    if True:
        raise UserDirectoryNotFound(
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
