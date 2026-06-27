"""Database session factory and helper dependency.

This module configures the SQLAlchemy engine and session factory and
exposes `get_db` which yields a session for use as a FastAPI
dependency. Sessions are closed after the request completes.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Database connection URL - in production this should come from
# configuration or environment variables rather than being hard-coded.
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(bind=engine)


def get_db():
    """Yield a SQLAlchemy `Session` and ensure it is closed afterwards.

    Use this function as a FastAPI dependency (via `Depends`) to get a
    transactional DB session for the duration of a request.
    """
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()