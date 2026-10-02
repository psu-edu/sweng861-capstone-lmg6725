from sqlalchemy import Boolean, Column, Integer, String, DateTime
from models.database import Base
from datetime import datetime, timezone


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True)

    patient_id = Column(String, nullable=False)

    doctor_id = Column(String, nullable=True)

    appointment_date = Column(DateTime, nullable=False)

    provider_name = Column(String)

    reason = Column(String)

    status = Column(String, default = "scheduled") # scheduled, completed, canceled

    patient_notes = Column(String)

    doctor_notes = Column(String)

    # Nice to have to notify pcp
    pcp_notification_requested = Column(Boolean, default=False)
    pcp_name = Column(String)
    pcp_email = Column(String)

    # Timestamp indicating when the appointment was created
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # Timestamp indicating when the appointment was last updated
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))