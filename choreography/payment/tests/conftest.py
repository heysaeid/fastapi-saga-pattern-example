import pytest_asyncio
from fastapi.testclient import TestClient
from src.app import create_app
from src.database import get_session, drop_and_create_all_tables
from src.repositories.payment import PaymentRepository
from src.services.payment import PaymentService
from src.schemas.payment import CreatePaymentSchema


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