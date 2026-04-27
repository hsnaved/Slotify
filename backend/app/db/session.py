from sqlalchemy import creat_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./slotify.db"
engine = creat_engine(DATABASE_URL)
sessionLocal = sessionmaker(bind = engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:        
        db.close()  