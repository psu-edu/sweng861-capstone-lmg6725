from sqlalchemy import inspect

from models.database import (Base, engine)

from models.provider import Provider


def main():
    inspector = inspect(engine)

    tables = inspector.get_table_names()

    if "providers" in tables:
        print(
            "providers table already exists. "
            "No changes made."
        )
        return

    Provider.__table__.create(
        bind=engine,
        checkfirst=True
    )

    print(
        "providers table created successfully. "
        "Existing database data was preserved."
    )


if __name__ == "__main__":
    main()