import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from src.app import create_app
from src.database import drop_and_create_all_tables, get_session
from src.repositories.payment import PaymentRepository
from src.schemas.payment import CreatePaymentSchema
from src.services.payment import PaymentService


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
def payment_repo(db_session):
    return PaymentRepository(db_session=db_session)


@pytest_asyncio.fixture
def payment_service(payment_repo):
    return PaymentService(payment_repo=payment_repo)


@pytest_asyncio.fixture
async def create_payment(payment_service):
    async def _create_payment(creation_data: CreatePaymentSchema):
        payment = await payment_service.create_payment(creation_data)
        return payment

    return _create_payment


@pytest.fixture
def mock_broker_publish(mocker):
    mock_publish = mocker.patch("services.payment.broker.publish", new=AsyncMock())
    yield mock_publish