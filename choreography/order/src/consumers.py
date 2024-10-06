from faststream import Depends, Logger
from services.order import OrderService
from repositories.order import OrderRepository
from schemas.order import (
    CancelOrderEventSchema,
    ConfirmOrderEventSchema,
    ConfirmOrderDeliveryEventSchema,
)
from utils.enums import KafkaTopicEnum
from database import get_session
from stream import broker


async def get_order_repository(db=Depends(get_session)):
    return OrderRepository(db)


async def get_order_service(order_repo=Depends(get_order_repository)):
    return OrderService(order_repo)


@broker.subscriber(
    KafkaTopicEnum.CONFIRM_ORDER, group_id=f"{KafkaTopicEnum.CONFIRM_ORDER}-grp"
)
async def handle_confirm_order_event(
    message: ConfirmOrderEventSchema,
    logger: Logger,
    order_service: OrderService = Depends(get_order_service),
):
    await order_service.confirm_order(message.order_id)
    logger.info(f"Order confirmed: {message}")


@broker.subscriber(
    KafkaTopicEnum.CONFIRM_ORDER_DELIVERY,
    group_id=f"{KafkaTopicEnum.CONFIRM_ORDER_DELIVERY}-grp",
)
async def handle_confirm_order_delivery(
    message: ConfirmOrderDeliveryEventSchema,
    logger: Logger,
    order_service: OrderService = Depends(get_order_service),
):
    await order_service.confirm_order_delivery(message.order_id)
    logger.info(f"The order was delivered: {message}")


@broker.subscriber(
    KafkaTopicEnum.CANCEL_ORDER, group_id=f"grp-{KafkaTopicEnum.CANCEL_ORDER}-grp"
)
async def handle_cancel_order_event(
    message: CancelOrderEventSchema,
    logger: Logger,
    order_service: OrderService = Depends(get_order_service),
):
    await order_service.cancel_order(message.order_id)
    logger.info(f"The order was cancelled: {message}")
