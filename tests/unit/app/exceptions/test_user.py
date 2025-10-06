import pytest

from app.exceptions.user import UserAlreadyExists, UserNotFound

# --- UserNotFound ---

def fake_UserNotFound_function():
    raise UserNotFound(
        "The user is not found!"
    )


def test_UserNotFound_is_raised():
    """
    GIVEN a UserNotFound exception
    WHEN fake_UserNotFound_function is called
    THEN it should raise UserNotFound
    """
    with pytest.raises(UserNotFound):
        fake_UserNotFound_function()

# --- UserAlreadyExists ---

def fake_UserAlreadyExists_function():
    raise UserAlreadyExists(
        "The user already exists!"
    )


def test_UserAlreadyExists_is_raised():
    """
    GIVEN a UserAlreadyExists exception
    WHEN fake_UserAlreadyExists_function is called
    THEN it should raise UserAlreadyExists
    """
    with pytest.raises(UserAlreadyExists):
        fake_UserAlreadyExists_function()
