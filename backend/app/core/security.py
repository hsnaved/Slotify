"""Security helpers for hashing and JWT token creation.

This module centralizes cryptographic operations used by the API such
as password hashing/verification and access token creation.
"""

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

# These constants control token encoding/decoding. In production the
# SECRET_KEY should be provided from secure configuration or environment.
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """Hash a plaintext password using the configured bcrypt context.

    Returns the hashed password string suitable for storage in the DB.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """Verify a plaintext password against a stored hash.

    Returns True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    """Create a JWT access token containing `data` as the payload.

    The token will include an expiration claim (`exp`) based on the
    configured `ACCESS_TOKEN_EXPIRE_MINUTES` and is encoded with
    `SECRET_KEY` and `ALGORITHM`.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)