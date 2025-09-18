import os

import httpx
import pytest

BASE_URL = os.getenv("API_BASE_URL")

@pytest.fixture(scope="module")
def http_client():
    """
        Provides a httpx client for the test module.
    """
    with httpx.Client(base_url=BASE_URL) as client:
        yield client
