import numpy as np
import pytest
import json
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from tests.app.helperfunc.helperfunc import get_test_image
from app.routers.image import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)

