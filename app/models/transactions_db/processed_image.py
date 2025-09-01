import uuid
from sqlmodel import SQLModel, Field,  Relationship
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Column, DateTime

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
    # <--- ...Keep this code together
    # Keep this code together... --->
    # Question: which UnprocessedImage does this image derive from?
    unprocessed_image_id: uuid.UUID = Field(
        # establishes the link the id column in user
        foreign_key="unprocessedimage.id",
        # ensure that every processed_image must associate with a unprocessed_image
        nullable=False,
        # add a database index to speed up queries that filter images by unprocessed_image
        index=True
    )
    # This is the corresponding relationship attribute to UnprocessedImage
    unprocessed_image: "UnprocessedImage" = Relationship(
        # 'back_populates' links this relationship to the 'unprocessed_image' field on the UnprocessedImage model.
        back_populates="processed_images"
    )
    # <--- ...Keep this code together
    # --- Table Relationships ---
    # This is the corresponding relationship attribute to ProcessingJob
    job: Optional["ProcessingJob"] = Relationship(
        # 'back_populates' links this relationship to the 'processed_image' field on the ProcessingJob model.
        back_populates="processed_image"
    )