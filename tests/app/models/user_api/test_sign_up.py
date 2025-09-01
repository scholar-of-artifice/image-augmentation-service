import uuid
from datetime import datetime
from app.models.user_api.sign_up import UserRead
import pytest

def test_user_read_successful_creation():
    """
        GIVEN a uuid
        AND a time
        AND an external_id
        WHEN a UserRead is created
        THEN it saves the correct information
    """
    # input variables
    user_id = uuid.uuid4()
    time_created = datetime.now()
    external_id = "auth0|some_unique_id_123"
    # create an instance of the model
    user = UserRead(
        id=user_id,
        external_id=external_id,
        created_at=time_created,
    )
    # assert that the fields were set correctly
    assert user.id == user_id
    assert user.external_id == external_id
    assert user.created_at == time_created

def test_ValidationError_when_user_read_is_missing_id():
    """
        GIVEN no uuid
        AND a time
        AND an external_id
        WHEN a UserRead is created
        THEN it raises an ValidationError
    """
    # input variables
    user_id = None
    time_created = datetime.now()
    external_id = "auth0|some_unique_id_123"
    # create an instance of the model
    user = UserRead(
        id=user_id,
        external_id=external_id,
        created_at=time_created,
    )
    # assert that the fields were set correctly
    assert user.id == user_id
    assert user.external_id == external_id
    assert user.created_at == time_created

def test_ValidationError_when_user_read_is_missing_created_at():
    """
        GIVEN a uuid
        AND no time
        AND an external_id
        WHEN a UserRead is created
        THEN it raises an ValidationError
    """
    # input variables
    user_id = uuid.uuid4()
    time_created = None
    external_id = "auth0|some_unique_id_123"
    # create an instance of the model
    user = UserRead(
        id=user_id,
        external_id=external_id,
        created_at=time_created,
    )
    # assert that the fields were set correctly
    assert user.id == user_id
    assert user.external_id == external_id
    assert user.created_at == time_created

def test_ValidationError_when_user_read_is_missing_external_id():
    """
        GIVEN a uuid
        AND a time
        AND no external_id
        WHEN a UserRead is created
        THEN it raises an ValidationError
    """
    # input variables
    user_id = uuid.uuid4()
    time_created = datetime.now()
    external_id = None
    # create an instance of the model
    user = UserRead(
        id=user_id,
        external_id=external_id,
        created_at=time_created,
    )
    # assert that the fields were set correctly
    assert user.id == user_id
    assert user.external_id == external_id
    assert user.created_at == time_created
