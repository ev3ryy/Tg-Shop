from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    BOT_TOKEN: str
    DATABASE_URL: str = "sqlite+aiosqlite:///database/shop.db"

settings = Settings()