from dataclasses import Field
from datetime import datetime
from sqlmodel import SQLModel

class ProcessedImage(SQLModel, table=True):
    """
    Class representing a processed image in the database.
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

