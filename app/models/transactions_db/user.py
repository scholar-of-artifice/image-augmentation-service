import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import func, Column, DateTime

class User(SQLModel, table=True):
    """
        Class representing a user in the database.

        NOTE: Authentication and Authorization are handled by an external service.
    """
    # Question: who is this user?
    # the unique identifier for this user in the database
    id: uuid.UUID | None = Field(
        # provides a function to generate a default value for new records
        default_factory=lambda: uuid.uuid4(),
        # marks this column as the primary key of this table
        primary_key=True,
        # tells the database to create an index on this column
        index=True,
        # is a constraint that ensures every user MUST have an ID
        nullable=False
    )
    # Question: What is the user's external id?
    # the external id from the external authentication provider (e.g., the 'sub' claim in a JWT)
    # this links our internal user record to the external authentication system.
    external_id: str = Field(
        # is a constraint that ensures no 2 users can have the same external_id
        unique=True,
        # tells the database to create an index on this column.
        index=True,
        # sets a maximum length for the external id
        max_length=255,
        # is a constraint that ensures every user MUST have an external id
        nullable=False
    )
    # Question: when was this user created?
    # the timestamp for when this user was created
    created_at: Optional[datetime] = Field(
        # automatically sets the creation time to the current time in UTC when a new user is added
        default_factory=lambda: datetime.now(timezone.utc),
        # tells SQLAlchemy to use a timezone-aware database column type
        sa_column=Column(
            # this ensures the database stores the date, time and timezone
            DateTime(timezone=True),
            # is a constraint that ensures every user MUST have a time they were inserted into this database
            nullable=False
        )
    )
    # Question: when was this record last updated?
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            # This tells the DB to update the field to the current time on any change
            onupdate=func.now()
        )
    )
    # --- Table Relationships ---
    # a User can have many UnprocessedImage records.
    unprocessed_images: List["UnprocessedImage"] = Relationship(
        # 'back_populates' links this relationship to the 'user' field on the UnprocessedImage model.
        back_populates="user",
        # These kwargs are passed to the underlying SQLAlchemy relationship
        sa_relationship_kwargs={
            # This ensures that if a User is deleted, all their associated
            # unprocessed_images are automatically deleted as well.
            "cascade": "all, delete-orphan"
        }
    )
    # a User can also have many ProcessedImage records.
    processed_images: List["ProcessedImage"] = Relationship(
        # 'back_populates' links this relationship to the 'user' field on the ProcessedImage model.
        back_populates="user",
        # These kwargs are passed to the underlying SQLAlchemy relationship
        sa_relationship_kwargs={
            # This ensures that if a User is deleted, all their associated
            # processed_images are automatically deleted as well.
            "cascade": "all, delete-orphan"
        }
    )