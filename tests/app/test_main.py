from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def app_includes_router_to_healthcheck_api_healthcheck_does_exist():
    """
        GIVEN the app is up
        WHEN /api/healthcheck-api/healthcheck/ is called
        THEN the app should respond with 404
    """
    response = client.get("/api/healthcheck-api/healthcheck/")
    assert response.status_code == status.HTTP_200_OK

def app_includes_router_to_image_api_info_does_not_exist():
    """
        GIVEN the app is up
        WHEN /api/image-api/info/ is called
        THEN the app should respond with 404
    """
    response = client.get("/api/image-api/info/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
