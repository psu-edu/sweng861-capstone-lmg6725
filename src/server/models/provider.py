from sqlalchemy import (Column, Integer, String, Boolean)

from models.database import Base


class Provider(Base):
    __tablename__ = "providers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False,
        unique=True
    )

    specialty = Column(
        String,
        nullable=False
    )

    service_category = Column(
        String,
        nullable=False
    )

    active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    def __repr__(self):
        return (
            f"<Provider("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"specialty='{self.specialty}'"
            f")>"
        )