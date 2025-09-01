from fastapi import (APIRouter, status)
from app.models.health_api.user import User
from app.models.logging import LogEntry
import logging
from datetime import datetime

router = APIRouter()
# set up logging
logger = logging.getLogger(__name__)

