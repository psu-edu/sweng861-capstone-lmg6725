import pytest

from main import app
from models.database import SessionLocal
from User import User


@pytest.fixture
def client():
    """Use the existing Flask application in testing mode."""
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def _delete_user_by_provider_id(provider_id):
    """Remove a leftover test user from an earlier interrupted test run."""
    db = SessionLocal()

    try:
        existing = (
            db.query(User)
            .filter(User.provider_id == provider_id)
            .first()
        )

        if existing:
            db.delete(existing)
            db.commit()
    finally:
        db.close()


@pytest.fixture
def patient_user():
    """Create a real patient User row that matches the Flask test session."""
    provider_id = "patient-123"
    _delete_user_by_provider_id(provider_id)

    db = SessionLocal()

    try:
        user = User(
            provider_id=provider_id,
            email="patient123@test.com",
            name="Test Patient",
            username="testpatient",
            password_hash="test-only",
            role="patient"
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        user_id = user.id
    finally:
        db.close()

    # Return a simple snapshot instead of an object attached to a closed
    # SQLAlchemy session.
    test_user = {
        "id": user_id,
        "provider_id": provider_id,
        "role": "patient"
    }

    yield test_user

    db = SessionLocal()

    try:
        saved_user = db.query(User).filter(User.id == user_id).first()

        if saved_user:
            db.delete(saved_user)
            db.commit()
    finally:
        db.close()


@pytest.fixture
def second_patient_user():
    """Create a second patient for ownership/403 tests."""
    provider_id = "different-patient-id"
    _delete_user_by_provider_id(provider_id)

    db = SessionLocal()

    try:
        user = User(
            provider_id=provider_id,
            email="patient2@test.com",
            name="Second Test Patient",
            username="testpatient2",
            password_hash="test-only",
            role="patient"
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        user_id = user.id
    finally:
        db.close()

    test_user = {
        "id": user_id,
        "provider_id": provider_id,
        "role": "patient"
    }

    yield test_user

    db = SessionLocal()

    try:
        saved_user = db.query(User).filter(User.id == user_id).first()

        if saved_user:
            db.delete(saved_user)
            db.commit()
    finally:
        db.close()


@pytest.fixture
def doctor_user():
    """Create a real doctor User row for doctor-only route tests."""
    provider_id = "doctor-123"
    _delete_user_by_provider_id(provider_id)

    db = SessionLocal()

    try:
        user = User(
            provider_id=provider_id,
            email="doctor123@test.com",
            name="Test Doctor",
            username="testdoctor",
            password_hash="test-only",
            role="doctor"
        )

        db.add(user)
        db.commit()
        db.refresh(user)
        user_id = user.id
    finally:
        db.close()

    test_user = {
        "id": user_id,
        "provider_id": provider_id,
        "role": "doctor"
    }

    yield test_user

    db = SessionLocal()

    try:
        saved_user = db.query(User).filter(User.id == user_id).first()

        if saved_user:
            db.delete(saved_user)
            db.commit()
    finally:
        db.close()


@pytest.fixture
def login_patient(client, patient_user):
    """Authenticate the test client as the created patient."""
    with client.session_transaction() as session:
        session["access_token"] = "fake-token"
        session["user_id"] = patient_user["provider_id"]

    return patient_user


@pytest.fixture
def login_doctor(client, doctor_user):
    """Authenticate the test client as the created doctor."""
    with client.session_transaction() as session:
        session["access_token"] = "fake-token"
        session["user_id"] = doctor_user["provider_id"]

    return doctor_user
