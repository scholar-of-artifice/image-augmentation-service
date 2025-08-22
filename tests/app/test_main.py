from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

