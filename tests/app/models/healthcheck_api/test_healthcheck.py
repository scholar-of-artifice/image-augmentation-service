import pytest
from pydantic import ValidationError
from app.models.healthcheck_api.healthcheck import HealthCheckResponse


def test_HealthCheckResponse_has_correct_structure():
    """
    GIVEN a HealthCheckResponse model
    WHEN a HealthCheckResponse is created with the correct structure
    THEN a HealthCheckResponse object is returned.
    """
    data = {
        "status": "OK",
    }
    obj = HealthCheckResponse(**data)
    assert obj.status == "OK"

def test_HealthCheckResponse_validates_incorrect_structure():
    """
    GIVEN a HealthCheckResponse model
    WHEN a HealthCheckResponse is created with an incorrect structure
    THEN a ValidationError is raised.
    """
    data = {
        "status": "ok",
    }
    with pytest.raises(ValidationError):
        HealthCheckResponse(**data)