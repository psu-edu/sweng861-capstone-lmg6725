from datetime import datetime, timedelta

from models.database import SessionLocal
from models.appointment import Appointment


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


def test_patient_gets_own_appointments(
    client,
    login_patient
):
    response = client.get(
        "/appointments/mine"
    )

    assert response.status_code == 200

def test_patient_cannot_get_doctor_appointment_list(
    client,
    login_patient
):
    response = client.get("/appointments")

    assert response.status_code == 403


def test_get_missing_appointment(
    client,
    login_patient
):
    response = client.get(
        "/appointments/999999"
    )

    assert response.status_code == 404



def test_get_existing_appointment(
    client,
    login_patient
):
    appointment_id = create_test_appointment(
        patient_id=
            login_patient["provider_id"]
    )

    response = client.get(
        f"/appointments/{appointment_id}"
    )

    assert response.status_code == 200

def test_user_can_access_own_appointment(
    client,
    login_patient
):
    appointment_id = create_test_appointment(
        patient_id=login_patient["provider_id"]
    )

    response = client.get(
        f"/appointments/{appointment_id}"
    )

    assert response.status_code == 200


def test_patient_cannot_access_another_patients_appointment(
    client,
    login_patient,
    second_patient_user
):
    appointment_id = create_test_appointment(
        patient_id=
            second_patient_user["provider_id"]
    )

    response = client.get(
        f"/appointments/{appointment_id}"
    )

    assert response.status_code == 403


def test_past_appointment_is_rejected(client, login_patient):

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


def test_duplicate_provider_time_is_rejected(client, login_patient):
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

def test_doctor_can_get_all_appointments(
    client,
    login_doctor
):
    response = client.get(
        "/appointments"
    )

    assert response.status_code == 200

