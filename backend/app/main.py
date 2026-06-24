"""Slotify FastAPI application entrypoint.

This module creates the FastAPI app instance, ensures database tables
are created on startup (via SQLAlchemy metadata) and mounts the
API routers for users, auth, businesses and services.
"""

from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
from app.api.routes import user, auth, business, service, availability_rule

app = FastAPI()

# create the database tables if they do not exist
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    """Health-check endpoint.

    Returns a small JSON payload used to verify the backend is running.
    """
    return {"message": "Slotify backend is running!"}


app.include_router(user.router)
app.include_router(auth.router)
app.include_router(business.router)
app.include_router(service.router)
app.include_router(availability_rule.router)