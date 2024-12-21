# app/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgres://postgres:postgres@localhost:5433/postgres"
 
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
