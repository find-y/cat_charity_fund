import logging
from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = "Default App title"
    app_description: Optional[str] = None
    database_url: str = "sqlite+aiosqlite:///./fastapi.db"
    secret: str = "default_secret_key"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = ".env"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


settings: Settings = Settings()
