from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar

class Settings(BaseSettings):
    DATABASE_URL: str = "postgres://postgres:postgres@localhost:5433/tornament"

    TORTOISE_ORM: ClassVar[dict] = {
        "connections": {"default": "postgres://postgres:postgres@localhost:5433/tornament"},
        "apps": {
            "models": {
                "models": ["app.models"],
                "default_connection": "default",
            },
        },
    }

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
