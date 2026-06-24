from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from app.db.base import Base


class AvailabilityRule(Base):
    __tablename__ = "availability_rules"

    id = Column(Integer, primary_key=True)

    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False
    )

    start_date = Column(Date)
    end_date = Column(Date)

    weekdays = Column(JSON)

    start_time = Column(Time)
    end_time = Column(Time)

    service = relationship(
        "Service",
        back_populates="availability_rules"
    )

    slots = relationship(
        "AvailabilitySlot",
        back_populates="rule",
        cascade="all, delete-orphan"
    )