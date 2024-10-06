import pytest
from src.models.order import OrderStatusEnum
from src.services.order import OrderService


@pytest.mark.asyncio
async def test_create_order(create_order, order_data, mock_broker_publish):
    created_order = await create_order(order_data)

    assert created_order is not None
    assert created_order.customer_id == order_data.customer_id
    assert created_order.total_amount == order_data.total_amount
    assert len(created_order.order_items) == 2
    assert (
        created_order.order_items[0].product_id == order_data.order_items[0].product_id
    )
    assert (
        created_order.order_items[1].product_id == order_data.order_items[1].product_id
    )
    mock_broker_publish.assert_called()


@pytest.mark.asyncio
async def test_confirm_order(
    order_service: OrderService, order_data, mock_broker_publish
):
    created_order = await order_service.create_order(order_data)
    confirmed_order = await order_service.confirm_order(created_order.id)
    assert confirmed_order.status == OrderStatusEnum.CONFIRMED
    mock_broker_publish.assert_called()


@pytest.mark.asyncio
async def test_confirm_order_delivery(
    order_service: OrderService, order_data, mock_broker_publish
):
    created_order = await order_service.create_order(order_data)
    confirmed_order = await order_service.confirm_order_delivery(created_order.id)
    assert confirmed_order.status == OrderStatusEnum.DELIVERED


@pytest.mark.asyncio
async def test_cancel_order(
    order_service: OrderService, order_data, mock_broker_publish
):
    created_order = await order_service.create_order(order_data)
    canceled_order = await order_service.cancel_order(created_order.id)
    assert canceled_order.status == OrderStatusEnum.CANCELLED
