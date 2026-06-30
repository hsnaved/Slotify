from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Business(Base):
    """SQLAlchemy model representing a business owned by a user."""
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    description = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="businesses")
    services = relationship("Service", back_populates="business")
    settings = relationship(
        "BusinessSettings",
        back_populates="business",
        uselist=False,
        cascade="all, delete-orphan"
    )