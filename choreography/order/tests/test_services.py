import pytest
from src.schemas.order import CreateOrderSchema, CreateOrderItem
from src.models.order import OrderStatusEnum


@pytest.mark.asyncio
async def test_create_order(create_order):
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

    created_order = await create_order(create_order_data)

    assert created_order is not None
    assert created_order.customer_id == create_order_data.customer_id
    assert created_order.total_amount == create_order_data.total_amount
    assert len(created_order.order_items) == 2
    assert created_order.order_items[0].product_id == order_items_data[0].product_id
    assert created_order.order_items[1].product_id == order_items_data[1].product_id


@pytest.mark.asyncio
async def test_cancel_order(order_service):
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
    created_order = await order_service.create_order(create_order_data)
    canceled_order = await order_service.cancel_order(created_order.id)
    assert canceled_order.status == OrderStatusEnum.CANCELLED
    assert canceled_order.id == created_order.id