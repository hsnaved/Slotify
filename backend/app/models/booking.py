from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Enum
)

from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from app.db.base import Base

from app.enums.booking_status import BookingStatus


class Booking(Base):
    """
    Represents a customer's appointment for a specific
    availability slot.
    """

    __tablename__ = "bookings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    slot_id = Column(
        Integer,
        ForeignKey("availability_slots.id"),
        nullable=False,
        unique=True
    )

    status = Column(
        Enum(BookingStatus),
        nullable=False,
        default=BookingStatus.BOOKED
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    customer = relationship(
        "User",
        back_populates="bookings"
    )

    slot = relationship(
        "AvailabilitySlot",
        back_populates="booking"
    )