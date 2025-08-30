import uuid
from sqlmodel import SQLModel, Field,  Relationship
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import JSONB

class ProcessedImage(SQLModel, table=True):
    """
        Class representing a processed image in the database.
    """
    # Question: which image is this?
    # this is the unique identifier of this processed image in the database
    id: uuid.UUID | None = Field(
        # generates a unique ID for each image upon creation.
        default_factory=lambda: uuid.uuid4(),
        # marks this column as the primary key of this table
        primary_key=True,
        # tells the database to create an index on this column
        index=True,
        # is a constraint that ensures every user MUST have an ID
        nullable=False
    )
    # Question: what is the uuid name of this image?
    # this is the storage filename of this image
    storage_filename: str = Field(
        # enforces that every image must have a unique storage filename.
        unique=True,
        # sets a maximum length for the filename
        max_length=255,
        # the image record must include a storage filename
        nullable=False
    )
    # Question: when was this image created?
    # this is a timestamp of when this image was created
    created_at: Optional[datetime] = Field(
        # automatically sets the creation time to the current time in UTC when a new user is added
        default_factory=lambda: datetime.now(timezone.utc),
        # This tells SQLAlchemy to use a timezone-aware database column type
        sa_column=Column(
            # this ensures the database stores the date, time and timezone
            DateTime(timezone=True),
            # the image record must include a created_at timestamp
            nullable=False
        )
    )
    # --- Table Associations ---
    # Question: who wrote this image?
    user_id: uuid.UUID = Field(
        # establishes the link the id column in user
        foreign_key="user.id",
        # ensure that every unprocessed model must associate with a user
        nullable=False,
        # add a database index to speed up queries that filter images by user
        index=True
    )
    # --- Table Relationships ---
    # This is the corresponding relationship attribute
    user: "User" = Relationship(
        # 'back_populates' links this relationship to the 'processed_images' field on the User model.
        back_populates="processed_images"
    )
    # what is the original image?
    # unprocessed_image_id: uuid.UUID = Field(foreign_key="unprocessed_image.id", nullable=False, index=True)
    # what processing_job created this image?
    # processing_job_id: uuid.UUID = Field(foreign_key="processing_job.id", nullable=False, index=True)