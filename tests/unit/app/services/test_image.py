import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.file_handling import InvalidImageFileError
from app.schemas.image import RotateArguments, ShiftArguments, UploadRequestBody, ResponseUploadImage
from app.schemas.transactions_db import UnprocessedImage, User

pytestmark = pytest.mark.asyncio

# TODO: write tests