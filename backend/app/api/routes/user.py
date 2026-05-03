from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_services import create_user_services

router = APIRouter()

@router.post("/users", response_model = UserResponse)
def create_user(user:UserCreate, db:Session = Depends(get_db)):
    return create_user_services(user, db)