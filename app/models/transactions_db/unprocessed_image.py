import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import Column, DateTime

class UnprocessedImage(SQLModel, table=True):
    """
        Class representing an unprocessed image in the database.
    """
    # Question: which image is this?
    # the unique identifier for this specific image record.
    id: uuid.UUID | None = Field(
        # generates a unique ID for each image upon creation.
        default_factory=lambda: uuid.uuid4(),
        # marks this column as the primary key of this table
        primary_key=True,
        # tells the database to create an index on this column
        index=True,
        # is a constraint that ensures every user MUST have an ID
        nullable=False,
    )
    # Question: what is the original name of this image?
    # the original filename as it was uploaded by the user (e.g., "holiday_photo.jpg").
    original_filename: str = Field(
        # the image record must include the original filename.
        nullable=False,
        # sets a minimum length for the filename
        min_length=1,
        # sets a maximum length for the filename
        max_length=255,
    )
    # Question: what is the uuid name of this image?
    # the new, unique filename assigned to the image when saved in storage.
    storage_filename: str = Field(
        # enforces that every image must have a unique storage filename.
        unique=True,
        # sets a maximum length for the filename
        max_length=255,
        # the image record must include a storage filename
        nullable=False
    )
    # Question: when was this image created?
    # the timestamp for when this image was uploaded
    created_at: Optional[datetime] = Field(
        # automatically sets the creation time to the current time in UTC when a new user is added
        default_factory=lambda: datetime.now(timezone.utc),
        # this tells SQLAlchemy to use a timezone-aware database column type
        sa_column=Column(
            # this ensures the database stores the date, time and timezone
            DateTime(timezone=True),
            # the image record must include a created_at timestamp
            nullable=False
        )
    )
    # Question: who wrote this image?
    # the foreign key linking this image to a record in the 'user' table.
    user_id: uuid.UUID = Field(
        # establishes the link the id column in user
        foreign_key="user.id",
        # ensure that every unprocessed model must associate with a user
        nullable=False,
        # add a database index to speed up queries that filter images by user
        index=True
    )
    # --- Table Relationships ---
    # an unprocessed image is related to a single user
    user: "User" = Relationship(
        # 'back_populates' links this relationship to the 'unprocessed_images' field on the User model.
        back_populates="unprocessed_images"
    )
    # an unprocessed image is related to multiple processed_images
    processed_images: List["ProcessedImage"] = Relationship(
        # 'back_populates' links this relationship to the 'unprocessed_image' field on the ProcessedImage model.
        back_populates="unprocessed_image"
    )
    # TODO: relationship