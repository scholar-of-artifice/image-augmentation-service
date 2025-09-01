from app.models.transactions_db.user import User
from app.models.transactions_db.unprocessed_image import UnprocessedImage
from app.models.transactions_db.processed_image import ProcessedImage
from app.models.transactions_db.job_status import JobStatus
from app.models.transactions_db.processing_job import ProcessingJob
from sqlmodel import Session
from datetime import datetime, timezone
import uuid
import pytest

def test_processing_job_is_valid(db_session: Session):
    """
        GIVEN a User and an UnprocessedImage exist in the database
        AND a valid ProcessingJob entry is created for them
        WHEN the ProcessingJob is inserted into the database
        THEN it persists correctly with the correct default values
    """
    # create a user and commit
    user = User(external_id='user-ext-1234')
    db_session.add(user)
    db_session.commit()
    # create an unprocessed_image and commit
    unprocessed_image = UnprocessedImage(
        user_id=user.id,
        original_filename="vacation_pic.png",
        storage_filename="some-storage-name.png"
    )
    db_session.add(unprocessed_image)
    db_session.commit()
    # create a processing_job
    job = ProcessingJob(
        user_id=user.id,
        unprocessed_image_id=unprocessed_image.id,
        upload_request_body={"filter": "sepia", "intensity": 0.8},
    )
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    # test the processing_job
    assert job.id is not None
    assert isinstance(job.id, uuid.UUID)
    assert job.user_id == user.id
    assert job.unprocessed_image_id == unprocessed_image.id
    assert job.upload_request_body["filter"] == "sepia"
    # test the default values
    assert job.job_status == JobStatus.PENDING
    assert isinstance(job.requested_at, datetime)
    assert job.requested_at.tzinfo == timezone.utc
    # test that nullable fields are None by default
    assert job.processed_image_id is None
    assert job.started_at is None
    assert job.completed_at is None