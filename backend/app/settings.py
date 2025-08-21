import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application Settings
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Database URL. For the SQLite workaround, this will be a file path.
    # e.g., "sqlite:///./sql_app.db"
    # The actual value will be loaded from the .env file.
    DATABASE_URL: str = "sqlite:////app/backend/sql_app.db"

    # External Services
    OPENAI_API_KEY: str | None = None
    STRIPE_API_KEY: str | None = None
    STRIPE_WEBHOOK_SECRET: str | None = None
    STRIPE_ESSENTIAL_PLAN_ID: str | None = None
    STRIPE_GROWTH_PLAN_ID: str | None = None
    STRIPE_SCALE_PLAN_ID: str | None = None

    class Config:
        # Using a relative path for the .env file as it's more portable.
        # The alembic env.py script is configured to load it from the project root.
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
