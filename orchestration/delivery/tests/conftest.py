import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from src.app import create_app
from src.database import drop_and_create_all_tables, get_session
from src.repositories.delivery import DeliveryRepository
from src.repositories.delivery_person import DeliveryPersonRepository
from src.services.delivery import DeliveryService
from src.services.delivery_person import DeliveryPersonService


@pytest_asyncio.fixture(autouse=True)
async def client():
    app = create_app()
    await drop_and_create_all_tables()
    return TestClient(app)


@pytest_asyncio.fixture
async def db_session():
    async for s in get_session():
        yield s


@pytest.fixture
def delivery_repo(db_session):
    return DeliveryRepository(db_session=db_session)


@pytest.fixture
def delivery_person_repo(db_session):
    return DeliveryPersonRepository(db_session=db_session)


@pytest.fixture
def delivery_person_service(delivery_person_repo):
    return DeliveryPersonService(delivery_person_repo)


@pytest.fixture
def delivery_service(delivery_repo, delivery_person_service):
    return DeliveryService(
        delivery_repo=delivery_repo,
        delivery_person_service=delivery_person_service,
    )
