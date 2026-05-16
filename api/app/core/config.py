from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "elegio-api"
    APP_ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str
    DATABASE_URL_SYNC: str

    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 60 * 24

    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
