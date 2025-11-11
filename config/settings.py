from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Updated to use local MongoDB to fix connection and CORS-related DNS issues
    MONGODB_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "skillsync"
    JWT_SECRET_KEY: str = "supersecretkey"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()