import enum
from pydantic import BaseModel, EmailStr

class UserRole(enum.Enum):
    admin = "admin"
    customer = "customer"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    number: str
    password: str
    role: UserRole

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    number: str
    role: UserRole

    class Config:
        from_attribute = True