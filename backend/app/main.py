from fastapi import FastAPI

from app.db.session import engine
from app.db.base import Base
from app.api.routes import user, auth

app = FastAPI()

#create the database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message":"Slotify backend is running!"}

app.include_router(user.router)
app.include_router(auth.router)