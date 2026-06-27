from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = "postgresql://postgres:jamundi@localhost:5432/slotify_db"

    class Config:
        env_file = ".env"
        

settings = Settings()