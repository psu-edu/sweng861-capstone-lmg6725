from datetime import datetime, timezone, timedelta
from flask import Blueprint, jsonify, redirect, request, session
from middleware.authMiddleware import require_auth
from middleware.roleMiddleware import require_role
from services.twilio_service import send_appointment_confirmation
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
@appointment_bp.route(
    "/appointments/slots",
    methods=["GET"]
)
@require_auth
@require_role("patient")
def get_available_slots():
    db = SessionLocal()

    try:
        now = datetime.now()
        end_date = now + timedelta(days=90)

        available_times = [
            (9, 0),
            (10, 0),
            (11, 0),
            (13, 0),
            (14, 0),
            (15, 0)
        ]

        # Get all doctor users
        providers = [
            "Dr. Alex",
            "Dr. Lauren",
            "Dr. Harrison",
            "Nurse Sharon",
            "Nurse Brandon",
            "Nurse Braxton",
            "Campus Health Center"
        ]

        # Get scheduled appointments once
        scheduled_appointments = (
            db.query(Appointment)
            .filter(
                Appointment.appointment_date >= now,
                Appointment.appointment_date <= end_date,
                Appointment.status == "scheduled"
            )
            .all()
        )

        # Fast lookup of unavailable slots
        booked_slots = {
            (
                appointment.provider_name,
                appointment.appointment_date
            )
            for appointment in scheduled_appointments
        }

        slots = []

        for day_offset in range(1, 91):

            day = now + timedelta(
                days=day_offset
            )

            # Skip Saturday and Sunday
            if day.weekday() >= 5:
                continue

            # Filter slots by provider
            for provider in providers:

                for hour, minute in available_times:

                    slot_datetime = day.replace(
                        hour=hour,
                        minute=minute,
                        second=0,
                        microsecond=0
                    )

                    slot_key = (
                        provider,
                        slot_datetime
                    )

                    if slot_key not in booked_slots:

                        slots.append({
                            "provider_name": provider,

                            "appointment_date":
                                slot_datetime.isoformat()
                        })

        return jsonify({
            "slots": slots
        }), 200

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        db.close()

# Book an appointment (for patients)
@appointment_bp.route("/appointments/book", methods=["POST"])
@require_auth
@require_role("patient")
def book_appointment():
    data = request.get_json()
    db = SessionLocal()

    try:
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
        
        max_appointment_date = datetime.now() + timedelta(days=90)

        if appointment_date > max_appointment_date:
            return jsonify({
                "error": (
                    "Appointments cannot be booked "
                    "more than 3 months in advance."
                )
            }), 400

        # Check if the appointment slot is already taken
        existing_appointment = (
            db.query(Appointment)
            .filter(
                Appointment.provider_name
                    == data.get("provider_name"),
                Appointment.appointment_date
                    == appointment_date,
                Appointment.status == "scheduled"
            )
            .first()
        )

        if existing_appointment:
            return jsonify({
                "error": (
                    "That appointment slot is no longer "
                    "available. Please select another."
                )
            }), 409

        db.add(appointment)
        db.commit()
        db.refresh(appointment)

        current_user = (db.query(User).filter(User.provider_id == g.user_id).first())

        # default sms sent variable
        sms_sent = False

        if current_user and current_user.phone_number:
            try:
                send_appointment_confirmation(
                    patient_phone =current_user.phone_number,
                    provider_name = appointment.provider_name,
                    appointment_date = appointment.appointment_date
                )

                sms_sent = True

            except Exception as sms_error:
                print(f"Error sending SMS: {sms_error}")


        return jsonify({
            "message": "Appointment booked successfully",
            "appointment_id": appointment.id,
            "sms_confirmation_sent": sms_sent
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500      

    finally:
        db.close()

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