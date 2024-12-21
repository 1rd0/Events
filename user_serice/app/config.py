# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgres://postgres:postgres@localhost:5433/postgres"
    JWT_SECRET_KEY: str = "secretBEKkey"  # Замените на ваш секретный ключ
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
