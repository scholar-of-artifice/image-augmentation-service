from dataclasses import Field
from sqlmodel import SQLModel
from datetime import datetime

class UnprocessedImage(SQLModel, table=True):
    """
    Class representing a unprocessed image in the database.
    """
    # which image is this?
    id: int = Field(primary_key=True)
    # what was this image named?
    file_name: str
    # where is this image stored?
    file_path: str
    # when was this image created?
    created_at: datetime
    # when was this image last read?
    last_accessed_at: datetime