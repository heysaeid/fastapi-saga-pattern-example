import pytest_asyncio
from fastapi.testclient import TestClient
from src.app import create_app
from src.database import get_session, drop_and_create_all_tables
from src.repositories.delivery import DeliveryRepository
from src.repositories.delivery_person import DeliveryPersonRepository
from src.services.delivery import DeliveryService


@pytest_asyncio.fixture(autouse=True)
async def client():
    app = create_app()
    await drop_and_create_all_tables()
    return TestClient(app)

@pytest_asyncio.fixture
async def db_session():
    async for s in get_session():
        yield s

@pytest_asyncio.fixture
def delivery_repo(db_session):
    return DeliveryRepository(db_session=db_session)


@pytest_asyncio.fixture
def delivery_person_repo(db_session):
    return DeliveryPersonRepository(db_session=db_session)

@pytest_asyncio.fixture
def delivery_service(delivery_repo, delivery_person_repo):
    return DeliveryService(
        delivery_repo=delivery_repo,
        delivery_person_repo=delivery_person_repo,
    )

@pytest_asyncio.fixture
async def create_delivery(delivery_service):
    async def _create_delivery(creation_data: CreatedeliverySchema):
        delivery = await delivery_service.create_delivery(creation_data)
        return delivery
    return _create_delivery