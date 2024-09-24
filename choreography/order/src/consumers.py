from faststream import Depends
from services.order import OrderService
from repositories.order import OrderRepository
from schemas.order import CancelOrderEventSchema
from utils.enums import KafkaTopicEnum
from database import get_session
from stream import broker


async def get_order_repository(db = Depends(get_session)):
    return OrderRepository(db)

async def get_order_service(order_repo = Depends(get_order_repository)):
    return OrderService(order_repo)


@broker.subscriber(KafkaTopicEnum.CONFIRMED_ORDER, group_id=f"grp-{KafkaTopicEnum.CONFIRMED_ORDER}")
async def handle_confirmed_order_event(
    message: CancelOrderEventSchema,
    order_service: OrderService = Depends(get_order_service),
):
    await order_service.confirmed_order(message.order_id)


@broker.subscriber(KafkaTopicEnum.CANCEL_ORDER, group_id=f"grp-{KafkaTopicEnum.CANCEL_ORDER}")
async def handle_cancel_order_event(
    message: CancelOrderEventSchema,
    order_service: OrderService = Depends(get_order_service),
):
    await order_service.cancel_order(message.order_id)
