
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import Column, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from .job_status import JobStatus
import uuid

class ProcessingJob(SQLModel, table=True):
    """
        Class representing a ProcessingJob in the database.
    """
    # which processing is this?
    id: int | None = Field(default=None, primary_key=True)
    # who requested this?
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    # what was the request?
    upload_request_body: Dict[str, Any] = Field(sa_column=Column(JSONB, nullable=False))
    # what image needs to be processed?
    unprocessed_image_id: int = Field(foreign_key="unprocessed_images.id", nullable=False)
    # what image was created?
    processed_image_id: int = Field(foreign_key="processed_images.id", nullable=True)
    # what is the status of this job?
    # Question: which processing is this?
    # the unique identifier for this specific image record.
    id: uuid.UUID | None = Field(
        # generates a unique ID for each image upon creation.
        default_factory=lambda: uuid.uuid4(),
        # marks this column as the primary key of this table
        primary_key=True,
        # tells the database to create an index on this column
        index=True,
        # is a constraint that ensures every ProcessingJob MUST have an ID
        nullable=False,
    )
    job_status: JobStatus = Field(
        sa_column=Column(Enum(JobStatus), nullable=False),
        default=JobStatus.PENDING
    )
    # when was this request made?
    requested_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False) # This tells SQLAlchemy to use a timezone-aware database column type
    )
    started_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)) # This tells SQLAlchemy to use a timezone-aware database column type
    )
    completed_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)) # This tells SQLAlchemy to use a timezone-aware database column type
    )