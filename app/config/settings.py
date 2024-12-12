import os
from decimal import Decimal
from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT")
    database_user: str = os.getenv("DATABASE_USER")
    database_password: str = os.getenv("DATABASE_PASSWORD")
    database_host: str = os.getenv("DATABASE_HOST")
    database_port: str = os.getenv("DATABASE_PORT")
    database_name: str = os.getenv("DATABASE_NAME")
    maximum_daily_limit: Decimal = os.getenv("MAXIMUM_DAILY_LIMIT", 2000.0)

@lru_cache
def get_settings():
    _settings = Settings()
    return _settings
