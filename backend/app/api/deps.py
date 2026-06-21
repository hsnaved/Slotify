from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.db.session import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM
from logging import getLogger


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

# Dependency to get the current user from the JWT token, login checking
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentails_exception = HTTPException(
        status_code = 401,
        detail = "Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms =[ALGORITHM])

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

# Authorization dependency to check if the user is an admin
def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code = 403,
            detail = "Admins only"
        )
    
    return current_user