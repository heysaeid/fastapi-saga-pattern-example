from fastapi.exceptions import HTTPException
from pydantic import PositiveInt
from models.order import Order, OrderItem
from repositories.order import OrderRepository
from schemas.order import CreateOrderSchema
from utils.stream import broker
from utils.enum import OrderStatusEnum
from choreography.order.src.utils.enum import KafkaTopicEnum
from choreography.order.src.schemas.order import CreatePaymentEventSchema


class OrderService:
    
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def get_order_or_404(self, order_id: PositiveInt):
        payment = await self.order_repo.get_by_id(order_id)
        if not payment:
            raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found.")
        return payment

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
        await broker.publish(
            topic=KafkaTopicEnum.CREATE_PAYMENT, 
            message=CreatePaymentEventSchema(
                order_id=order.id,
                amount=order.total_amount,
            ),
        )
        return order

    async def cancel_order(self, order_id: PositiveInt):
        order = await self.get_order_or_404(order_id)
        order.status = OrderStatusEnum.CANCELLED
        await self.order_repo.update(order, commit=True)
        return order
