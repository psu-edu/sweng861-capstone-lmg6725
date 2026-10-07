from datetime import datetime
from unittest.mock import patch

import pytest
import requests

from models.database import SessionLocal
from models.appointment import Appointment


def test_ai_endpoint_missing_key(client):
    response = client.post(
        "/ask-ai",
        json={
            "prompt": "Hello"
        }
    )

    assert response.status_code in [400, 401, 500]


@pytest.mark.parametrize(
    "user_request, expected_service, expected_time",
    [
        ("I need to make an appointment.", "General Visit", "any"),
        ("I need a flu shot after lunch.", "Vaccination", "afternoon"),
        ("I hurt my ankle and prefer mornings.", "Sports Injury", "morning"),
        ("I need a routine physical.", "Wellness Visit", "any"),
        ("I need a checkup before lunch.", "Wellness Visit", "morning"),
    ],
)
def test_ai_development_fallback_classification(
    client,
    user_request,
    expected_service,
    expected_time,
):
    """Verify the development fallback classifies the raw user request.

    The real Drift request is forced to fail with ConnectionError so this test
    does not depend on the external class-provided AI service being online.
    """

    # /ask-ai requires an authenticated session.
    with client.session_transaction() as session:
        session["access_token"] = "fake-token"
        session["user_id"] = "patient-123"

    # Force the real Drift call to be unavailable so the fallback runs.
    with patch(
        "routes.apiRoutes.ask_drift",
        side_effect=requests.exceptions.ConnectionError("Drift unavailable")
    ):
        response = client.post(
            "/ask-ai",
            json={
                "prompt": "Scheduling classifier instructions",
                "user_request": user_request,
            },
        )

    # The fallback should keep the route usable.
    assert response.status_code == 200

    data = response.get_json()
    assert data["development_fallback"] is True

    content = data["choices"][0]["message"]["content"]
    assert f"SERVICE_CATEGORY: {expected_service}" in content
    assert f"TIME_PREFERENCE: {expected_time}" in content


def test_get_appointment_includes_provider_and_date(client):
    db = SessionLocal()
    appointment = Appointment(
        patient_id="patient-123",
        appointment_date=datetime(2026, 9, 17, 14, 30),
        provider_name="Dr. Alex",
        reason="Follow-up",
        patient_notes="Needs review",
        doctor_notes="Updated notes",
        status="scheduled",
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    db.close()

    with client.session_transaction() as session:
        session["access_token"] = "fake-token"
        session["user_id"] = "patient-123"

    response = client.get(f"/appointments/{appointment.id}")

    assert response.status_code == 200
    data = response.get_json()
    assert data["provider_name"] == "Dr. Alex"
    assert data["appointment_date"] is not None

