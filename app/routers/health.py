from fastapi import (APIRouter, status)
from app.models.health_api.healthcheck import HealthCheckResponse

router = APIRouter()

@router.get(path="/healthcheck",
         status_code=status.HTTP_200_OK)
def get_health():
    return HealthCheckResponse(status="OK")