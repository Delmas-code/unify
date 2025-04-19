from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Unify"
    DEBUG: bool = False

    # Database settings
    DATABASE_URL: str = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else "mongodb://localhost:27017"
    DATABASE_NAME: str = os.environ["DATABASE_NAME"] if "DATABASE_NAME" in os.environ else "unify_db"

    # Security settings
    SECRET_KEY: str = os.environ["SECRET_KEY"] if "SECRET_KEY" in os.environ else "your_secret_key"
    JWT_ALGORITHM: str = os.environ["JWT_ALGORITHM"] if "JWT_ALGORITHM" in os.environ else "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]) if "ACCESS_TOKEN_EXPIRE_MINUTES" in os.environ else 30

    # Other settings
    ENVIRONMENT: str = "development"  # Options: development, production, testing

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a settings instance
settings = Settings()
