from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.enums.user_role import UserRole


class User(Base):
    """SQLAlchemy model representing an application user.

    Fields include authentication information (hashed password) and a
    `role` enum used for authorization decisions.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    number = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)

    businesses = relationship("Business", back_populates="owner")
