import sqlite3
from pathlib import Path
from sqlalchemy import create_engine
from models import Base
from models.appointment import Appointment

database_path = Path(__file__).with_name("users.db")
columns = {
    "patient_notes": "TEXT",
    "doctor_notes": "TEXT",
    "pcp_notification_requested": "BOOLEAN DEFAULT 0",
    "pcp_name": "TEXT",
    "pcp_email": "TEXT",
}

sqlite_engine = create_engine(f"sqlite:///{database_path.as_posix()}")
Base.metadata.create_all(bind=sqlite_engine)
sqlite_engine.dispose()

with sqlite3.connect(database_path) as conn:
    cursor = conn.cursor()
    existing_columns = {
        row[1] for row in cursor.execute("PRAGMA table_info(appointments)")
    }

    for column_name, column_definition in columns.items():
        if column_name not in existing_columns:
            cursor.execute(
                f"ALTER TABLE appointments ADD COLUMN {column_name} {column_definition}"
            )
            print(f"Added {column_name}")
        else:
            print(f"{column_name} already exists")

print(f"Updated {database_path}")