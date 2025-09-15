from typing import Literal

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """
        Response model to validate and return when performing a health check.
    """
    status: Literal["OK"]