import enum

class JobStatus(str, enum.Enum):
    """
        Enum for state of jobs.

        SUCCEEDED AND FAILED are both valid end states.
    """
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
