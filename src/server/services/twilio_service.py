from twilio.rest import Client

from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER
)


def send_appointment_confirmation(
    patient_phone,
    provider_name,
    appointment_date
):
    client = Client(
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN
    )

    message = client.messages.create(
        to=patient_phone,
        from_=TWILIO_PHONE_NUMBER,
        body="sms_appointment_reminders"
    )

    return message.sid