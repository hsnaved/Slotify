from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError   
from fastapi import HTTPException

from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password

def create_user_services(user_data:UserCreate, db:Session):
    user = User(
        username = user_data.username,
        email = user_data.email,
        number = user_data.number,
        hashed_password = hash_password(user_data.password),
        role = user_data.role
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail = "Email/Number already exists"
        )
