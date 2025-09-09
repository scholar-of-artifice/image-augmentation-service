from pydantic import BaseModel
from typing import Literal

class HealthCheckResponse(BaseModel):
    """
        Response model to validate and return when performing a health check.
    """
    status: Literal["OK"]