from sqlalchemy import DateTime
from sqlalchemy import Column, Integer, String
from datetime import datetime, timezone
from models.database import Base

# User model represents a user stored in the database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True) # Unique identifier for each user
    provider_id = Column(String) # Identifier for the authentication provider
    email = Column(String, unique=True) # User's email address
    name = Column(String) # User's name
    username = Column(String(50), unique = True, nullable = True) # OAuth does not provide username
    password_hash = Column(String(255), nullable = True) # OAuth does not provide password hash
    role = Column(String(20), default="patient")
    phone_number = Column(String, nullable=True)

    # Timestamp indicating when the user was created
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    # Timestamp indicating when the user last logged in
    last_login = Column(DateTime, default=lambda: datetime.now(timezone.utc))