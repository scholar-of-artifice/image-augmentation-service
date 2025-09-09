import pytest
from app.schemas.transactions_db.job_status import JobStatus

def test_JobStatus_member_values():
    """
        GIVEN a JobStatus
        WHEN accessing the value of each member
        THEN the correct string value should be returned
    """
    assert JobStatus.PENDING.value == "pending"
    assert JobStatus.PROCESSING.value == "processing"
    assert JobStatus.SUCCEEDED.value == "succeeded"
    assert JobStatus.FAILED.value == "failed"

def test_JobStatus_string_equality():
    """
        GIVEN a JobStatus
        WHEN comparing a member to its string equivalent
        THEN they should be equal
    """
    assert JobStatus.PENDING == "pending"
    assert JobStatus.PROCESSING == "processing"
    assert JobStatus.SUCCEEDED == "succeeded"
    assert JobStatus.FAILED == "failed"

def test_JobStatus_instantiation_from_string():
    """
        GIVEN a JobStatus enum
        WHEN a valid string is used to instantiate a member
        THEN the correct enum member should be returned
    """
    assert JobStatus("pending") is JobStatus.PENDING
    assert JobStatus("processing") is JobStatus.PROCESSING
    assert JobStatus("succeeded") is JobStatus.SUCCEEDED
    assert JobStatus("failed") is JobStatus.FAILED

def test_JobStatus_invalid_status_raises_error():
    """
        GIVEN a JobStatus enum
        WHEN an invalid string is used to instantiate a member
        THEN a ValueError should be raised
    """
    with pytest.raises(ValueError, match="'in_progress' is not a valid JobStatus"):
        JobStatus("in_progress")

def test_JobStatus_inheritance():
    """
        GIVEN a JobStatus enum
        WHEN checking the type of a member
        THEN it should be an instance of both JobStatus and str
    """
    assert isinstance(JobStatus.FAILED, JobStatus)
    assert isinstance(JobStatus.FAILED, str)
