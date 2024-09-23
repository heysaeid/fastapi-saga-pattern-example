from utils.stream import broker
from fastapi import Depends
from database import get_session
from src.repositories.order import OrderRepository
from src.services.order import OrderService
from src.schemas.order import CancelOrderEventSchema
from src.utils.enum import KafkaTopicEnum


def get_order_service(db = Depends(get_session)):
    order_repo = OrderRepository(db)
    return OrderService(order_repo)


@broker.subscriber(KafkaTopicEnum.CANCEL_ORDER, group_id=f"grp_{KafkaTopicEnum.CANCEL_ORDER}")
async def handle_cancel_order_event(
    message: CancelOrderEventSchema,
    order_service: OrderService = Depends(get_order_service),
):
    order_id = message["order_id"]
    await order_service.cancel_order(order_id)
    print(f"Order canceled: {order_id}")