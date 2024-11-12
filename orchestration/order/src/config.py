from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    app_env: str = "dev"
    app_name: str = 'Order'
    app_port: int = 8000
    debug: bool = True
    description: str = ''
    sqlalchemy_db_url: str = 'sqlite+aiosqlite:///order.db'
    broker_url: str = 'localhost:29092'


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
