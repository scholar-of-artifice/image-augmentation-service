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
    id: uuid.UUID | None = Field(
        default_factory=lambda: uuid.uuid4(),
        primary_key=True,
        index=True,
        nullable=False
    )
    # what is the uuid name of this image?
    storage_filename: str = Field(default_factory=lambda: f"{str(uuid.uuid4())}.png" , unique=True, nullable=False, max_length=40)
    # when was this image created?
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        # This tells SQLAlchemy to use a timezone-aware database column type
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    # --- Table Associations ---
    # who wrote this image?
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False, index=True)