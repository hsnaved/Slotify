from sqlalchemy import Column, Integer, String,Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.schemas.user import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    number = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole),default = UserRole.customer)

    businesses = relationship("Business", back_populates="owner")
