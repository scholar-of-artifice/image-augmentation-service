import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.internal.database import get_session
from app.models.transactions_db.user import User
from app.models.user_api.create import UserRead
from app.dependency import get_current_external_user_id

router = APIRouter()
# set up logging
logger = logging.getLogger(__name__)

