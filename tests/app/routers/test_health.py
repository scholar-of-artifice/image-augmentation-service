from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from app.routers.health import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_healthcheck_is_successful_when_request_is_valid():
    """
    GIVEN a client
    AND an endpoint of /healthcheck
    WHEN a get request is made to the endpoint
    THEN the correct response is returned.
    """
    response = client.get("/healthcheck")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}