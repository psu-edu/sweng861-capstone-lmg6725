from datetime import datetime

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

