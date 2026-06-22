"""API dependency helpers for authentication and authorization.

This module exposes FastAPI dependencies used by route functions to
extract and validate the currently authenticated user and to enforce
role-based checks such as admin-only access.
"""

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.session import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM
from logging import getLogger


# The OAuth2PasswordBearer dependency uses the token URL for the login
# route which is expected to return an access token when given valid
# credentials.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Resolve the current user from the provided JWT access token.

    This dependency decodes the JWT using the configured secret and
    algorithm, extracts the subject (`sub`) claim (user id), and
    loads the corresponding `User` instance from the database. If the
    token is invalid or the user is not found, an HTTP 401 is raised.
    """
    credentails_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        getLogger(__name__).info(f"Decoded JWT payload: {payload}")

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentails_exception

    except JWTError:
        raise credentails_exception

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise credentails_exception

    return user


def admin_only(current_user: User = Depends(get_current_user)):
    """Authorization dependency that allows only admin users.

    Raises HTTP 403 if the resolved `current_user` does not have the
    `admin` role. Returns the `current_user` when the check succeeds so
    it can be used in the route function.
    """
    if current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Admins only")

    return current_user