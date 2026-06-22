from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth_service import login_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate a user and return an access token.

    The endpoint expects form-encoded OAuth2 credentials (username and
    password) and delegates authentication to `login_user` returning the
    token dictionary on success.
    """
    return login_user(db, form_data.username, form_data.password)