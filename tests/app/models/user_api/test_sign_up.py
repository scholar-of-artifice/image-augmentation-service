import uuid
from datetime import datetime
from app.models.user_api.sign_up import UserRead

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
