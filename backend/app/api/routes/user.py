from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_services import create_user_services
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user from the provided `UserCreate` schema.

    Delegates the creation logic to the `create_user_services` service
    and returns the persisted `User` model (which is then serialized
    to the `UserResponse` schema by FastAPI).
    """
    return create_user_services(user, db)


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Return a small representation of the currently authenticated
    user.
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }