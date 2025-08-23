from fastapi import (APIRouter, status)
from app.models.health_api.healthcheck import HealthCheckResponse
from app.models.logging import LogEntry
import logging

router = APIRouter()
# set up logging
logger = logging.getLogger(__name__)

@router.get(path="/healthcheck",
         status_code=status.HTTP_200_OK)
def get_health():
    return HealthCheckResponse(status="OK")