from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: Literal["local", "dev", "prod"] = "local"
    log_level: str = "INFO"

    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")

    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@postgres:5432/betting_bot",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")

    digest_times_utc: list[str] = Field(default_factory=lambda: ["09:00", "12:00", "15:00", "18:00", "20:00"])
    min_odds: float = 1.3
    max_odds: float = 3.5
    confidence_threshold: float = 0.55
    enabled_sports: list[str] = Field(default_factory=lambda: ["football", "hockey", "tennis", "basketball", "mma"])
    enabled_leagues: list[str] = Field(default_factory=list)
    upcoming_window_hours: int = 24

    default_user_timezone: str = "UTC"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
