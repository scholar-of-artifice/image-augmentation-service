from unittest.mock import AsyncMock
import io
import pytest
from fastapi import status
from pydantic import ValidationError
from pathlib import Path
from app.dependency.async_dependency import get_current_active_user
from app.main import app
from app.schemas.image import ResponseUploadImage, ShiftArguments, UploadRequestBody
from app.schemas.transactions_db import UnprocessedImage
from app.schemas.transactions_db.user import User
import uuid

pytestmark = pytest.mark.asyncio

# --- upload_endpoint ---

# --- augment_endpoint ---

# --- get_unprocessed_image_by_id_endpoint ---

# --- get_processed_image_by_id_endpoint ---

# --- get_unprocessed_image_by_id_endpoint ---
