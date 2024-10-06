from pydantic import PositiveInt
from models.order import Order, OrderItem
from repositories.order import OrderRepository
from schemas.order import (
    CreateOrderSchema,
    CreatePaymentEventSchema,
    CreateDeliveryEventSchema,
)
from utils.enums import KafkaTopicEnum, OrderStatusEnum
from utils.exceptions import NotFoundException
from stream import broker


class OrderService:
    def __init__(self, order_repo: OrderRepository):
        self.order_repo = order_repo

    async def get_order_or_404(self, order_id: PositiveInt):
        payment = await self.order_repo.get_by_id(order_id)
        if not payment:
            raise NotFoundException
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
        )
        await broker.publish(
            topic=KafkaTopicEnum.CREATE_PAYMENT,
            message=CreatePaymentEventSchema.model_validate(order),
        )
        return order

    async def confirm_order(self, order_id: PositiveInt):
        order = await self._update_order_status(order_id, OrderStatusEnum.CONFIRMED)
        await broker.publish(
            topic=KafkaTopicEnum.CREATED_DELIVERY,
            message=CreateDeliveryEventSchema.model_validate(order),
        )
        return order
    
    async def confirm_order_delivery(self, order_id: PositiveInt):
        return await self._update_order_status(order_id, OrderStatusEnum.DELIVERED)

    async def cancel_order(self, order_id: PositiveInt):
        return await self._update_order_status(order_id, OrderStatusEnum.CANCELLED)

    async def _update_order_status(self, order_id: PositiveInt, status: OrderStatusEnum):
        order = await self.get_order_or_404(order_id)
        order = await self.order_repo.update(order, status=status)
        return order
