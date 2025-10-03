import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    """
        This is the model that will be returned to the client.
        It includes the fields that are safe to expose.
    """
    # The user's unique internal identifier in the database.
    id: uuid.UUID
    # The user's unique identifier in the external authentication service.
    external_id: str
    # The timestamp indicating when the user record was first created.
    created_at: datetime
    # This tells Pydantic to read the data from ORM model attributes,
    # So it can read data from `db_user.id`.
    model_config = ConfigDict(from_attributes=True)


# --- Endpoint Responses ---

class ResponseCreateUser(BaseModel):
    """
    This is the model that will be returned to the client.
    It includes the fields that are safe to expose.
    This response corresponds with:
        /sign-up/
    """
    # the ID of the user in the database.
    id: uuid.UUID
    # the external_id the user shows for authorization
    external_id: str