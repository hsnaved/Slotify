from sqlalchemy import Column, Integer, ForeignKey, DateTime, Date, Time, Boolean
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship


from app.db.base import Base

class AvailabilitySlot(Base):
    __tablename__ = "availability_slots"

    id = Column(Integer, primary_key=True)

    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False
    )

    rule_id = Column(
        Integer,
        ForeignKey("availability_rules.id"),
        nullable=False
    )

    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)

    is_booked = Column(Boolean, default=False)

    service = relationship(
        "Service",
        back_populates="availability_slots"
    )

    rule = relationship(
        "AvailabilityRule",
        back_populates="slots"
    )
