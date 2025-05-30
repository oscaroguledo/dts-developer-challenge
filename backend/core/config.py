# settings.py
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import List, Union
import os, json

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = 'tasks_db'
    DOMAIN: str = 'localhost'
    ENVIRONMENT: str
    SECRET_KEY: str
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = Field(default=[])

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def split_origins(cls, value):
        if isinstance(value, str) and value.startswith("["):
            return json.loads(value)
        elif isinstance(value, str):
            return [origin.strip() for origin in value.split(",")]
        return value

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def DATABASE_URL(self) -> str:
        print(self.POSTGRES_SERVER,'---')
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

# Initialize settings by reading from environment or .env file
settings = Settings()
