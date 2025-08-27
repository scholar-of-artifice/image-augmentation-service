import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, DateTime

class UnprocessedImage(SQLModel, table=True):
    """
        Class representing an unprocessed image in the database.
    """
    # which image is this?
    id: uuid.UUID | None = Field(
        default_factory=lambda: uuid.uuid4(),
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
    )
    # what is the original name of this image?
    original_filename: str = Field(nullable=False, max_length=255)
    # what is the uuid name of this image?
    storage_filename: str = Field(unique=True, nullable=False, max_length=255)
    # when was this image created?
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False) # This tells SQLAlchemy to use a timezone-aware database column type
    )
