
from sqlmodel import SQLModel, Field, Relationship
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
    # Question: what was the request?
    upload_request_body: Dict[str, Any] = Field(
        sa_column=Column(
            # postgres has a jsonb string
            # reference: https://www.postgresql.org/docs/current/datatype-json.html
            JSONB,
            # is a constraint that ensures we store the request for how to process a particular image
            nullable=False
        )
    )
    # Question: what image needs to be processed?
    unprocessed_image_id: uuid.UUID = Field(
        # establishes the link the id column in unprocessed_images
        foreign_key="unprocessedimage.id",
        # is a constraint that ensures every ProcessingJob MUST have an associated unprocessed_images
        nullable=False
    )
    # Question: what image was created?
    processed_image_id: Optional[uuid.UUID] = Field(
        # establishes the link the id column in processed_images
        foreign_key="processedimage.id",
        # is a constraint that ensures every ProcessingJob MUST have an associated processed_images
        nullable=True
    )
    # Question: what is the status of this job?
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
        sa_column=Column(
            # this tells SQLAlchemy to use a timezone-aware database column type
            DateTime(timezone=True),
            # is a constraint that ensures every ProcessingJob does not have an associated started_at until defined by the application
            nullable=True
        )
    )
    # --- Table Relationships ---
    # n processing_job is related to a single user
    user: "User" = Relationship(
        # 'back_populates' links this relationship to the 'unprocessed_images' field on the User model.
        back_populates="jobs"
    )
    # a processing_job is related to a single unprocessed_image
    unprocessed_image: "UnprocessedImage" = Relationship(
        # 'back_populates' links this relationship to the 'unprocessed_image' field on the UnprocessedImage model.
        back_populates="job"
    )
    # processing_job is related to a single processed_image
    processed_image: Optional["ProcessedImage"] = Relationship(
        # 'back_populates' links this relationship to the 'processed_image' field on the ProcessedImage model.
        back_populates="job"
    )