from enum import Enum
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppEnvironmentEnum(str, Enum):
    DEVELOPMENT = 'dev'
    PRODUCTION = 'prod'
    TEST = 'test'

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    app_env: str = AppEnvironmentEnum.DEVELOPMENT
    app_name: str = 'Delivery'
    app_port: int = 8000
    debug: bool = True
    description: str = ''
    sqlalchemy_db_url: str = 'sqlite+aiosqlite:///deliverydb.sql'
    broker_url: str = 'localhost:29092'


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
