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
    
    payment_service_url: str = "localhost:8001"
    delivery_service_url: str = "localhost:8002"
    
    create_payment_endpoint: str = payment_service_url + "/payments/create_payment"
    confirm_payment_endpoint: str = payment_service_url + "/payments/{product_id}/confirm"
    cancel_payment_endpoint: str = payment_service_url + "/payments/{product_id}/cancel"
    create_delivery_endpoint: str = delivery_service_url + "/deliveries/create_delivery"


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
