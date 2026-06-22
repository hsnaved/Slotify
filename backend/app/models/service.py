from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Service(Base):
    """SQLAlchemy model for a service offered by a business."""
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    duration_minutes = Column(Integer)
    business_id = Column(Integer, ForeignKey("businesses.id"))

    business = relationship("Business", back_populates="services")

    availability_rules = relationship(
        "AvailabilityRule",
        back_populates="service"
    )

    availability_slots = relationship(
        "AvailabilitySlot",
        back_populates="service"
    )