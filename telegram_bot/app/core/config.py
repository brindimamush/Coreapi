from pydantic_settings import BaseSettings

class BotSettings(BaseSettings):
    BOT_TOKEN: str
    WEBHOOK_URL: str = ""   # set in production
    CORE_API_URL: str = "http://localhost:8000/api/v1"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = BotSettings()