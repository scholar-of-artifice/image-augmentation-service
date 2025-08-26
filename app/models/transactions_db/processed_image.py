import uuid
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, DateTime

class ProcessedImage(SQLModel, table=True):
    """
        Class representing a processed image in the database.
    """
    # which image is this?
    id: int | None = Field(default=None, primary_key=True)
    # what is the uuid name of this image?
    storage_filename: str = Field(default_factory=lambda: f"{str(uuid.uuid4())}.png" , unique=True, nullable=False, max_length=40)
    # when was this image created?
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False) # This tells SQLAlchemy to use a timezone-aware database column type
    )