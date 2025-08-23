from fastapi import (APIRouter, status)
from app.models.health_api.healthcheck import HealthCheckResponse
from app.models.logging import LogEntry
import logging
from datetime import datetime

router = APIRouter()
# set up logging
logger = logging.getLogger(__name__)

@router.get(path="/healthcheck",
         status_code=status.HTTP_200_OK)
def get_health():
    log_data = LogEntry(
        date_time=datetime.now(),
        event="get_health",
        details="Health check"
    )
    logger.info(log_data.model_dump_json())
    return HealthCheckResponse(status="OK")