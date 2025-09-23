from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from app.routers.health import router

app = FastAPI()
app.include_router(router)

client = TestClient(app)


def test_healthcheck_is_successful_when_request_is_valid():
    """
    GIVEN a client
    AND an endpoint of .../healthcheck
    WHEN a get request is made to the endpoint
    THEN the correct status code is returned.
    """
    response = client.get("/healthcheck")
    assert response.status_code == status.HTTP_200_OK


def test_healthcheck_has_correct_response_when_request_is_valid():
    """
    GIVEN a client
    AND an endpoint of .../healthcheck
    WHEN a get request is made to the endpoint
    THEN the correct response is returned.
    """
    response = client.get("/healthcheck")
    assert response.json() == {"status": "OK"}


def test_healthcheck_is_unsuccessful_when_endpoint_does_not_exist():
    """
    GIVEN a client
    AND an endpoint of .../this-endpoint-does-not-exist
    WHEN a get request is made to the endpoint
    THEN a 404 is returned.
    """
    response = client.get("/this-endpoint-does-not-exist")
    assert response.status_code == status.HTTP_404_NOT_FOUND
