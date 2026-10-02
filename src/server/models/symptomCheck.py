from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base


class SymptomCheck(Base):
    __tablename__ = "symptom_checks"

    id = Column(Integer, primary_key=True)

    user_id = Column(String)

    symptoms = Column(Text)

    ai_response = Column(Text) # DRIFT AI response

    created_at = Column(DateTime)