from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base
from app.enums.cancellation_policy import CancellationPolicy


class BusinessSettings(Base):
    """
    Stores configurable business policies.
    """

    __tablename__ = "business_settings"

    id = Column(Integer, primary_key=True)

    business_id = Column(
        Integer,
        ForeignKey("businesses.id"),
        unique=True,
        nullable=False
    )

    requires_booking_approval = Column(
        Boolean,
        default=False,
        nullable=False
    )

    customer_cancellation_window_minutes = Column(
        Integer,
        default=30,
        nullable=False
    )

    allow_customer_cancellation = Column(
        Boolean,
        default=True,
        nullable=False
    )

    allow_owner_cancellation = Column(
        Boolean,
        default=True,
        nullable=False
    )

    cancellation_policy = Column(
        Enum(CancellationPolicy),
        default=CancellationPolicy.REOPEN_SLOT,
        nullable=False
    )

    timezone = Column(
        String,
        default="Asia/Kolkata",
        nullable=False
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

    business = relationship(
        "Business",
        back_populates="settings"
    )