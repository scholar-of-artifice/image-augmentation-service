import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import Column, DateTime
from pydantic import field_validator

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
    # Question: What is the user's unique id?
    # the unique id from the external authentication provider (e.g., the 'sub' claim in a JWT)
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
    # TODO: this validator is necessary because a min_length specification for external_id fails to evaluate
    # this custom validator ensures the field is never blank
    @field_validator("external_id")
    @classmethod
    def validate_external_id_is_not_blank(cls, v: str) -> str:
        # We use .strip() to also catch strings containing only whitespace
        if not v.strip():
            raise ValueError("external_id cannot be a blank string")
        return v
    # --- Table Relationships ---
    # a User can have many UnprocessedImage records.
    unprocessed_images: List["UnprocessedImage"] = Relationship(
        # 'back_populates' links this relationship to the 'user' field on the UnprocessedImage model.
        back_populates="user"
    )
    # a User can also have many ProcessedImage records.
    processed_images: List["ProcessedImage"] = Relationship(
        # 'back_populates' links this relationship to the 'user' field on the ProcessedImage model.
        back_populates="user"
    )