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

    #META Ad platform settings
    META_USER_ACCESS_TOKEN: str = os.environ["META_USER_ACCESS_TOKEN"] if "META_USER_ACCESS_TOKEN" in os.environ else "your_meta_app_access_token"
    META_BASE_URL: str = os.environ["META_BASE_URL"] if "META_BASE_URL" in os.environ else "https://graph.facebook.com/v22.0"
    META_AD_ACCOUNT_ID: str = os.environ["META_AD_ACCOUNT_ID"] if "META_AD_ACCOUNT_ID" in os.environ else "your_ad_account_id"
    #Invore(100945682247560)
    #Bickdrim Sandbox Ad Account (711620734622441)
    # Other settings
    ENVIRONMENT: str = "development"  # Options: development, production, testing

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a settings instance
settings = Settings()
