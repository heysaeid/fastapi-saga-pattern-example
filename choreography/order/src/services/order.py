from fastapi.exceptions import HTTPException
from pydantic import PositiveInt
from models.order import Order, OrderItem
from repositories.order import OrderRepository
from schemas.order import CreateOrderSchema, CreatePaymentEventSchema, CreateDeliveryEventSchema
from utils.enums import KafkaTopicEnum, OrderStatusEnum
from stream import broker


class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def get_order_or_404(self, order_id: PositiveInt):
        payment = await self.order_repo.get_by_id(order_id)
        if not payment:
            raise HTTPException(
                status_code=404, detail=f"Order with id {order_id} not found."
            )
        return payment

    async def create_order(
        self,
        creation_data: CreateOrderSchema,
    ):
        data = creation_data.model_dump()
        order_items = data.pop("order_items")
        order = await self.order_repo.create(
            entity=Order(
                order_items=[OrderItem(**item) for item in order_items], **data
            ),
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

    async def confirmed_order(self, order_id):
        order = await self.get_order_or_404(order_id)
        order.status = OrderStatusEnum.CONFIRMED
        await self.order_repo.update(order, commit=True)
        await broker.publish(
            topic=KafkaTopicEnum.CREATED_DELIVERY,
            message=CreateDeliveryEventSchema(
                order_id=order.id,
                province=order.province,
                city=order.city,
            ),
        )
        return order

    async def cancel_order(self, order_id: PositiveInt):
        order = await self.get_order_or_404(order_id)
        order.status = OrderStatusEnum.CANCELLED
        await self.order_repo.update(order, commit=True)
        return order
