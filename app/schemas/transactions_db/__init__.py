# Runtime Model Discovery
# A more robust, long-term solution is to create an __init__.py file in your schemas directory that imports all your schemas.
# This turns your schemas folder into a package that pre-loads all tables.

from .job_status import JobStatus
from .processed_image import ProcessedImage
from .processing_job import ProcessingJob
from .unprocessed_image import UnprocessedImage
from .user import User
