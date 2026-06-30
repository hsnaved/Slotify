from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables or the local .env file."""

    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # DATABASE_URL: str = "postgresql://postgres:jamundi@localhost:5432/slotify_db"
    DATABASE_URL: str = "postgresql://neondb_owner:npg_HSnZ6RtaFb0Q@ep-icy-star-at2g8l2p-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

    class Config:
        env_file = ".env"
        

settings = Settings()