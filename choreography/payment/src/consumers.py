from faststream import Depends, Logger
from repositories.payment import PaymentRepository
from services.payment import PaymentService
from schemas.payment import CreatePaymentEventSchema, CancelPaymentEventSchema
from utils.enums import KafkaTopicEnum
from database import get_session
from stream import broker


def get_payment_service(db=Depends(get_session)):
    payment_repo = PaymentRepository(db)
    return PaymentService(payment_repo)


@broker.subscriber(
    KafkaTopicEnum.CREATE_PAYMENT, group_id=f"{KafkaTopicEnum.CREATE_PAYMENT}-grp"
)
async def handle_create_payment_event(
    message: CreatePaymentEventSchema,
    logger: Logger,
    payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    
    await payment_service.create_payment(message)
    logger.info(f"New payment created: {message}")


@broker.subscriber(
    KafkaTopicEnum.CANCEL_PAYMENT, group_id=f"{KafkaTopicEnum.CANCEL_PAYMENT}-grp"
)
async def handle_cancel_payment_event(
    message: CancelPaymentEventSchema,
    logger: Logger,
    payment_service: PaymentService = Depends(get_payment_service),
) -> None:
    await payment_service.cancel_payment(message.payment_id)
    logger.info(f"The payment was cancelled: {message}")
