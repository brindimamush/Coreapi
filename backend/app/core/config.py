import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Core Verification Platform"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"   # development, testing, production

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/core_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT (future)
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"

    # Telegram Bot
    BOT_TOKEN: str = ""
    BOT_WEBHOOK_URL: str = ""

    # CORS origins
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()