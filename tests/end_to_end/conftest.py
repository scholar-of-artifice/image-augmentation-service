import os

import httpx
import pytest_asyncio

BASE_URL = os.getenv("API_BASE_URL")

@pytest_asyncio.fixture(scope="module")
async def http_client():
    """
        Provides an async httpx client for the test module.
    """
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        yield client
