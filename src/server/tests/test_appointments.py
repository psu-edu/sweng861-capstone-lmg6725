from datetime import datetime, timedelta

from models.database import SessionLocal
from models.appointment import Appointment


def authenticate(client, user_id="patient-123"):
    """Add the session values used by the application's auth middleware."""
    with client.session_transaction() as sess:
        sess["access_token"] = "test-token"
        sess["user_id"] = user_id


def create_test_appointment(
    patient_id="patient-123",
    provider_name="Dr. Smith",
    appointment_date=None,
    status="scheduled",
):
    """Create an appointment used by route tests."""
    if appointment_date is None:
        appointment_date = datetime.now() + timedelta(days=7)

    db = SessionLocal()
    appointment = Appointment(
        patient_id=patient_id,
        appointment_date=appointment_date,
        provider_name=provider_name,
        reason="Checkup",
        status=status,
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    appointment_id = appointment.id

    db.close()

    return appointment_id


def test_appointments_require_auth(client):
    response = client.get("/appointments")
    assert response.status_code == 401


def test_patient_gets_own_appointments(client):
    """Patients now use /appointments/mine instead of the doctor list."""
    authenticate(client)

    response = client.get("/appointments/mine")

    assert response.status_code == 200


def test_patient_cannot_get_doctor_appointment_list(client):
    """The all-appointments route is reserved for doctors."""
    authenticate(client)

    response = client.get("/appointments")

    assert response.status_code == 403


def test_get_missing_appointment(client):
    authenticate(client)

    response = client.get("/appointments/999999")

    assert response.status_code == 404


def test_get_existing_appointment(client):
    appointment_id = create_test_appointment()
    authenticate(client)

    response = client.get(
        f"/appointments/{appointment_id}"
    )

    assert response.status_code == 200

def test_user_can_access_own_appointment(client):
    appointment_id = create_test_appointment(
        patient_id="patient-123"
    )
    authenticate(client, "patient-123")

    response = client.get(
        f"/appointments/{appointment_id}"
    )

    assert response.status_code == 200


def test_patient_cannot_access_another_patients_appointment(client):
    """A patient must receive 403 for another patient's visit record."""
    appointment_id = create_test_appointment(
        patient_id="different-patient-id"
    )
    authenticate(client, "patient-123")

    response = client.get(
        f"/appointments/{appointment_id}"
    )

    assert response.status_code == 403


def test_past_appointment_is_rejected(client):
    authenticate(client)

    past_date = (
        datetime.now() - timedelta(days=1)
    ).replace(microsecond=0)

    response = client.post(
        "/appointments/book",
        json={
            "provider_name": "Campus Health Center",
            "appointment_date": past_date.isoformat(),
            "reason": "General Visit",
            "patient_notes": "",
            "pcp_notification_requested": False,
        },
    )

    assert response.status_code == 400
    assert "past" in response.get_json()["error"].lower()


def test_duplicate_provider_time_is_rejected(client):
    """Two scheduled visits cannot occupy the same provider/date/time slot."""
    future_date = (
        datetime.now() + timedelta(days=7)
    ).replace(
        hour=10,
        minute=0,
        second=0,
        microsecond=0,
    )

    # Put the conflicting appointment in the real test database used by the
    # existing suite, then submit the same provider/date/time through the API.
    create_test_appointment(
        patient_id="someone-else",
        provider_name="Campus Health Center",
        appointment_date=future_date,
        status="scheduled",
    )

    authenticate(client)

    response = client.post(
        "/appointments/book",
        json={
            "provider_name": "Campus Health Center",
            "appointment_date": future_date.isoformat(),
            "reason": "General Visit",
            "patient_notes": "",
            "pcp_notification_requested": False,
        },
    )

    assert response.status_code == 409
