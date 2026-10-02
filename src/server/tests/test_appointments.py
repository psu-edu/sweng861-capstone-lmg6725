from datetime import datetime
from models.database import SessionLocal
from models.appointment import Appointment


def test_appointments_require_auth(client):

    response = client.get("/appointments")

    assert response.status_code == 401

def test_get_appointments_authenticated(client):

    with client.session_transaction() as sess:
        sess["access_token"] = "token"
        sess["user_id"] = "patient-123"

    response = client.get("/appointments")

    assert response.status_code == 200

def test_get_missing_appointment(client):

    with client.session_transaction() as sess:
        sess["access_token"] = "test-token"
        sess["user_id"] = "patient-123"

    response = client.get("/appointments/999999")

    assert response.status_code == 404

def test_get_existing_appointment(client):

    db = SessionLocal()

    appointment = Appointment(
        patient_id="patient-123",
        appointment_date=datetime(2026, 11, 1, 10, 0),
        provider_name="Dr. Smith",
        reason="Checkup",
        status="scheduled"
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    appointment_id = appointment.id

    db.close()

    with client.session_transaction() as sess:
        sess["access_token"] = "token"
        sess["user_id"] = "patient-123"

    response = client.get(
        f"/appointments/{appointment_id}"
    )

    assert response.status_code == 200

def test_user_can_access_own_appointment(client):

    db = SessionLocal()

    appointment = Appointment(
        patient_id="patient-123",
        appointment_date=datetime(2026, 11, 1, 10, 0),
        provider_name="Dr. Smith",
        reason="Checkup",
        status="scheduled"
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    appointment_id = appointment.id

    db.close()

    with client.session_transaction() as sess:
        sess["access_token"] = "test-token"
        sess["user_id"] = "patient-123"

    response = client.get(
        f"/appointments/{appointment_id}"
    )

    assert response.status_code == 200
