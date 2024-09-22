from models.order import Order, OrderItem
from repositories.order import OrderRepository
from schemas.order import CreateOrderSchema
from utils.stream import broker


class OrderService:
    
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def create_order(
        self,
        creation_data: CreateOrderSchema,
    ):
        data = creation_data.model_dump()
        order_items = data.pop("order_items")
        order = await self.order_repo.create(
            entity=Order(order_items = [OrderItem(**item) for item in order_items], **data),
            commit=True,
        )
        await broker.publish(topic="create-payment", message={
            "order_id": order.id,
            "amount": order.amount,
        })
        return order
