from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:jamundi@localhost:5432/slotify_db"
engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(bind = engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:        
        db.close()  