from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional

class UnprocessedImage(SQLModel, table=True):
    """
    Class representing a unprocessed image in the database.
    """
    # which image is this?
    id: int | None = Field(default=None, primary_key=True)
    # who wrote this image?
    author_id: int = Field(nullable=False, index=True)
    # what is the original name of this image?
    original_filename: str = Field(nullable=False)
    # what is the uuid name of this image?
    storage_filename: str = Field(unique=True, nullable=False)
    # where is this image stored?
    storage_filepath: str = Field(unique=True, nullable=False)
    # when was this image created?
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)