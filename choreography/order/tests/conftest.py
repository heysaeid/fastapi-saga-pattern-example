import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from src.app import create_app
from src.database import get_session, drop_and_create_all_tables
from src.repositories.order import OrderRepository
from src.services.order import OrderService
from src.schemas.order import CreateOrderItem, CreateOrderSchema
from src.utils.enums import OrderStatusEnum


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
def order_repo(db_session):
    return OrderRepository(db_session=db_session)


@pytest_asyncio.fixture
def order_service(order_repo):
    return OrderService(order_repo=order_repo)


@pytest_asyncio.fixture
async def create_order(order_service):
    async def _create_order(creation_data: CreateOrderItem):
        payment = await order_service.create_order(creation_data)
        return payment

    return _create_order


@pytest.fixture
def mock_broker_publish(mocker):
    mock_publish = mocker.patch("services.order.broker.publish", new=AsyncMock())
    yield mock_publish


@pytest.fixture
def order_data():
    order_items_data = [
        CreateOrderItem(product_id=1, quantity=2, unit_price=100.0),
        CreateOrderItem(product_id=2, quantity=1, unit_price=200.0),
    ]
    create_order_data = CreateOrderSchema(
        customer_id=123,
        status=OrderStatusEnum.PENDING,
        total_amount=300.0,
        order_items=order_items_data,
        province="Tehran",
        city="Tehran",
    )
    return create_order_data
