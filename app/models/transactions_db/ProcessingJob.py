import enum
from dataclasses import Field
from sqlmodel import SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from app.models.image_api.upload import UploadRequestBody

class JobStatus(str, enum.Enum):
    """
        Enum for state of jobs.

        SUCCEEDED AND FAILED are both valid end states.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class ProcessingJob(SQLModel, table=True):
    """
        Class representing a processing job in the database.
    """
    # which processing job is this?
    id: int = Field(primary_key=True)
    # how is this processing jobs working out?
    status: JobStatus = Field(JobStatus.PENDING)
    # what was the user asking for?
    request_parameters: UploadRequestBody = Field(sa_column=Column(JSONB))
    # when was this request made?
    created_at: Optional[datetime] = Field(default=None)
    # when was this job started?
    started_at: Optional[datetime] = Field(default=None)
    # when did this job finish?
    finished_at: Optional[datetime] = Field(default=None)


