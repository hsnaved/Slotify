from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.core.security import create_access_token, verify_password


def login_user(db: Session, email: str, password: str):
    """Authenticate credentials and return an access token dict.

    Raises HTTP 400 on invalid credentials. On success returns a
    dictionary containing `access_token` and `token_type` which is the
    standard OAuth2 response shape used by the frontend.
    """
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}
