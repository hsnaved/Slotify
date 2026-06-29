import enum
from pydantic import BaseModel, EmailStr
from app.enums.user_role import UserRole

class UserCreate(BaseModel):
    """Request schema for creating a new user."""
    username: str
    email: EmailStr
    number: str
    password: str
    role: UserRole


class UserResponse(BaseModel):
    """Response schema returned when a user is serialized.

    Note: the nested `Config` class below enables reading attributes
    from ORM model instances; ensure the correct attribute flag is
    used for your Pydantic version (e.g. `orm_mode` or
    `from_attributes`).
    """
    id: int
    username: str
    email: EmailStr
    number: str
    role: UserRole

    class Config:
        # Some projects use `orm_mode = True`; this code uses the newer
        # `from_attributes` flag in Pydantic v2. Adjust to your runtime
        # Pydantic version if serialization doesn't behave as expected.
        from_attribute = True