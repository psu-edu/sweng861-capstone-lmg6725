from datetime import datetime, timezone
from flask import Blueprint, jsonify, redirect, request, session
from middleware.authMiddleware import require_auth
from middleware.roleMiddleware import require_role
from models.appointment import Appointment
from config import OKTA_REDIRECT_URL
from models.database import SessionLocal
from User import User
from flask import g
from extensions import limiter, oauth
from passlib.hash import bcrypt


#Blueprint for all appointment-related API endpoints
appointment_bp = Blueprint("appointment", __name__)

# Get available appointment slots (for patients)
@appointment_bp.route("/appointments/slots", methods=["GET"])
@require_auth
def get_available_slots():
    # testing
    slots = [
        {"date": "2024-07-01", "time": "09:00 AM"},
        {"date": "2024-07-01", "time": "10:00 AM"},
        {"date": "2024-07-01", "time": "11:00 AM"}
    ]
    return jsonify({"slots": slots})

# Book an appointment (for patients)
@appointment_bp.route("/appointments/book", methods=["POST"])
@require_auth
@require_role("patient")
def book_appointment():
    data = request.get_json()
    db = SessionLocal()
    appointment_date = datetime.fromisoformat(data.get("appointment_date"))
    # Logic to book an appointment
    appointment = Appointment(
        patient_id = g.user_id,
        #doctor_id=data.get("doctor_id"),
        appointment_date=appointment_date,
        provider_name=data.get("provider_name"),
        reason=data.get("reason"), 
        patient_notes=data.get("patient_notes"),
        status="scheduled",

        # Notify PCP
        pcp_notification_requested=data.get("pcp_notification_requested", False),
        pcp_name=data.get("pcp_name"),
        pcp_email=data.get("pcp_email")

    )
    # Check date
    if appointment_date < datetime.now():
        return jsonify({
            "error": "Appointments cannot be booked in the past"
            }), 400

    db.add(appointment)
    db.commit()
    db.close()
    return jsonify({"message": "Appointment booked successfully"}), 201

# Cancel an appointment (for patients)
@appointment_bp.route("/appointments/<int:id>/cancel",methods=["PUT"])
@require_auth
@require_role("patient") 
def cancel_appointment(id):

    db = SessionLocal()

    appointment = db.query(Appointment).filter(Appointment.id == id).first()

    if not appointment:
        return jsonify({
            "error": "Not found"
        }), 404

    appointment.status = "cancelled"

    db.commit()
    db.close()

    return jsonify({"message": "Appointment canceled successfully"}), 200

# Reschedule an appointment (for patients)
@appointment_bp.route( "/appointments/<int:id>/reschedule", methods=["PUT"])
@require_auth
@require_role("patient")
def reschedule_appointment(id):

    data = request.get_json()

    db = SessionLocal()

    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == id)
        .first()
    )

    if not appointment:
        db.close()
        return jsonify({
            "error": "Appointment not found"
        }), 404

    appointment.appointment_date = datetime.fromisoformat(
        data["appointment_date"]
    )

    appointment.status = "scheduled"

    db.commit()
    db.close()

    return jsonify({"message": "Appointment rescheduled successfully"}), 200

# View appointment details (for patients and doctors)
@appointment_bp.route("/appointments/<int:id>",methods=["GET"])
@require_auth
def get_appointment(id):

    db = SessionLocal()

    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == id)
        .first()
    )

    if not appointment:
        db.close()
        return jsonify({
            "error": "Appointment not found"
        }), 404
    
    # Data that shows when view details is pressed
    result = {
        "id": appointment.id,
        "patient_notes": appointment.patient_notes,
        "doctor_notes": appointment.doctor_notes,
        "reason": appointment.reason,
        "status": appointment.status,
        "provider_name": appointment.provider_name,
        "appointment_date": appointment.appointment_date.isoformat() if appointment.appointment_date else None,
    }

    db.close()

    return jsonify(result)

# Doctor can view all appointments for their patients
@appointment_bp.route("/appointments", methods=["GET"])
@require_auth
#@require_role("doctor")
def get_user_appointments():
    db = SessionLocal()
    appointments = db.query(Appointment).all()
    # Logic to retrieve appointments for the authenticated user
    allAppointments = [
        {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            #"doctor_id": appointment.doctor_id,
            "appointment_date": appointment.appointment_date,
            "provider_name": appointment.provider_name,
            "reason": appointment.reason,
            "patient_notes": appointment.patient_notes,
            "doctor_notes": appointment.doctor_notes,
            "status": appointment.status,
            "pcp_notification_requested": appointment.pcp_notification_requested,
            "pcp_name": appointment.pcp_name,
            "pcp_email": appointment.pcp_email,
        }
        for appointment in appointments
    ]
    db.close()
    return jsonify({"appointments": allAppointments}) 

# Update doctor notes for an appointment (for doctors)
@appointment_bp.route("/appointments/<int:id>/notes",methods=["PUT"])
@require_auth
@require_role("doctor")
def update_doctor_notes(id):

    data = request.get_json()

    db = SessionLocal()

    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == id)
        .first()
    )

    if not appointment:
        db.close()
        return jsonify({
            "error": "Appointment not found"
        }), 404

    appointment.doctor_notes = data["doctor_notes"]

    db.commit()
    db.close()

    return jsonify({ "message": "Doctor notes updated"}), 200