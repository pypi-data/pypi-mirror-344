import os
from typing import Optional

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    # ---------------------------------------------------Project Config-------------------------------------------------
    VERSION: str = "1.0.0"
    PROJECT_NAME: str = "Demo-FastAPI"
    API_PREFIX = '/api'
    DEBUG: bool = os.getenv("DEBUG", False)

    # ---------------------------------------------------Database Config------------------------------------------------
    POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB = os.getenv("POSTGRES", "mydatabase")
    DB_HOST = os.getenv("DATABASE_HOST", "pgbouncer")  # Default 'db' matches Docker Compose service name
    DB_PORT = os.getenv("DATABASE_PORT", "5432")

    # Construct the full database URL for Tortoise ORM
    DATABASE_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
    # add more configuration options as needed

    # ---------------------------------------------------Auth Config----------------------------------------------------
    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

    AUTH_MODEL = "src.auth.models.User"  # your user model
    AUTH_FIELD = "username"  # field used for authentication

    class Config:
        env_file = ".env"


settings = Settings()
