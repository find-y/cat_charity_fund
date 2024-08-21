from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Default App title"
    app_description: Optional[str] = None
    database_url: str
    secret_key: str = "default_secret_key"

    class Config:
        env_file = ".env"


settings = Settings()