import uuid
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import JSONB

class ProcessedImage(SQLModel, table=True):
    """
        Class representing a processed image in the database.
    """
    # which image is this?
    id: uuid.UUID | None = Field(
        default_factory=lambda: uuid.uuid4(),
        primary_key=True,
        index=True,
        nullable=False
    )
    # what is the uuid name of this image?
    storage_filename: str = Field(unique=True, nullable=False, max_length=255)
    # when was this image created?
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        # This tells SQLAlchemy to use a timezone-aware database column type
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    # --- Table Associations ---
    # who wrote this image?
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)
    # what is the original image?
    # unprocessed_image_id: uuid.UUID = Field(foreign_key="unprocessed_image.id", nullable=False, index=True)
    # what processing_job created this image?
    # processing_job_id: uuid.UUID = Field(foreign_key="processing_job.id", nullable=False, index=True)