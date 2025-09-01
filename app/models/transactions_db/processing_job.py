
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
    # Question: who requested this?
    user_id: uuid.UUID = Field(
        # establishes the link the id column in user
        foreign_key="user.id",
        # tells the database to create an index on this column
        index=True,
        # is a constraint that ensures every ProcessingJob MUST have an associated user
        nullable=False,
    )
    # Question: what image needs to be processed?
    unprocessed_image_id: uuid.UUID = Field(
        # establishes the link the id column in unprocessed_images
        foreign_key="unprocessedimage.id",
        # is a constraint that ensures every ProcessingJob MUST have an associated unprocessed_images
        nullable=False
    )
    job_status: JobStatus = Field(
        sa_column=Column(
            # use the JobStatus enum to define what the job status can be
            Enum(JobStatus),
            # is a constraint that ensures every ProcessingJob MUST have an associated job_status
            nullable=False
        ),
        default=JobStatus.PENDING
    )
    # Question: when was this request made?
    requested_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(
            # this tells SQLAlchemy to use a timezone-aware database column type
            DateTime(timezone=True),
            # is a constraint that ensures every ProcessingJob MUST have an associated requested_at
            nullable=False
        )
    )
    # Question: when did the processing for this image start?
    started_at: Optional[datetime] = Field(
        sa_column=Column(
            # this tells SQLAlchemy to use a timezone-aware database column type
            DateTime(timezone=True),
            # is a constraint that ensures every ProcessingJob does not have an associated started_at until defined by the application
            nullable=True
        )
    )
    # Question: when did the processing for this image complete?
    completed_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(timezone=True)) # This tells SQLAlchemy to use a timezone-aware database column type
    )