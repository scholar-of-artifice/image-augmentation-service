import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import Column, DateTime

class User(SQLModel, table=True):
    """
        Class representing a user in the database.

        NOTE: Authentication and Authorization are handled by an external service.
    """
    # which user is this?
    id: uuid.UUID | None = Field(
        default_factory=lambda: uuid.uuid4(),
        primary_key=True,
        index=True,
        nullable=False
    )
    # What is the user's unique id?
    # The unique id from the external authentication provider (e.g., the 'sub' claim in a JWT)
    external_id: str = Field(unique=True, index=True, nullable=False)
    # when was this user created?
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        # This tells SQLAlchemy to use a timezone-aware database column type
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )