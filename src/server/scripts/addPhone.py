"""Add phone_number column to the existing users table without deleting data.

Run from src/server with the project's virtual environment active:
    python add_phone_number_column.py
"""

from sqlalchemy import inspect, text
from models.database import engine


def main():
    inspector = inspect(engine)

    if "users" not in inspector.get_table_names():
        raise RuntimeError("The users table does not exist in the configured database.")

    columns = {column["name"] for column in inspector.get_columns("users")}

    if "phone_number" in columns:
        print("users.phone_number already exists. No changes made.")
        return

    with engine.begin() as connection:
        connection.execute(
            text("ALTER TABLE users ADD COLUMN phone_number VARCHAR")
        )

    print("Added users.phone_number successfully. Existing rows and data were preserved.")


if __name__ == "__main__":
    main()
