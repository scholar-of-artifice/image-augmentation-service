import pytest

from app.exceptions import PermissionDenied


def fake_PermissionDenied_function():
    raise PermissionDenied(
        "You do not have permission to do that!"
    )

def test_PermissionDenied_is_raised():
    """
    GIVEN a PermissionDenied exception
    WHEN fake_PermissionDenied_function is called
    THEN it should raise PermissionDenied
    """
    with pytest.raises(PermissionDenied):
        fake_PermissionDenied_function()