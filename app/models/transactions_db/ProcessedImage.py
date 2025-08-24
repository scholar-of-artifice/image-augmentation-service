from dataclasses import Field
from datetime import datetime
from sqlmodel import SQLModel

class ProcessedImage(SQLModel, table=True):
    """
    Class representing a processed image in the database.
    """
    id: int = Field(primary_key=True)   # which image is this?
    file_name: str                      # what was this image named?
    file_path: str                      # where is this image stored?
    created_at: datetime                # when was this image created?
    last_accessed_at: datetime          # when was this image last read?

