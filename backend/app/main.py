"""Slotify FastAPI application entrypoint.

This module creates the FastAPI app instance, ensures database tables
are created on startup (via SQLAlchemy metadata) and mounts the
API routers for users, auth, businesses and services.
"""

from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
from app.api.routes import user, auth, business, service, availability_rule, booking, business_settings

app = FastAPI()

# create the database tables if they do not exist
# Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    """Health-check endpoint.

    Returns a small JSON payload used to verify the backend is running.
    """
    return {"message": "Slotify backend is running!"}


app.include_router(user.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(business.router, prefix="/api/v1")
app.include_router(service.router, prefix="/api/v1")
app.include_router(availability_rule.router, prefix="/api/v1")
app.include_router(booking.router, prefix="/api/v1")
app.include_router(business_settings.router, prefix="/api/v1")