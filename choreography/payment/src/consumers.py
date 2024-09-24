from fastapi import Depends
from repositories.payment import PaymentRepository
from services.payment import PaymentService
from schemas.payment import CreatePaymentSchema, CreatePaymentEventSchema, CancelPaymentEventSchema
from utils.enums import KafkaTopicEnum
from database import get_session
from stream import broker



def get_payment_service(db = Depends(get_session)):
    payment_repo = PaymentRepository(db)
    return PaymentService(payment_repo)


@broker.subscriber(KafkaTopicEnum.CREATE_PAYMENT, group_id=f"grp-{KafkaTopicEnum.CREATE_PAYMENT}")
async def handle_create_payment_event(
    message: CreatePaymentEventSchema,
    payment_service: PaymentService = Depends(get_payment_service),
):
    await payment_service.create_payment(message)


@broker.subscriber(KafkaTopicEnum.CANCEL_PAYMENT, group_id=f"grp-{KafkaTopicEnum.CANCEL_PAYMENT}")
async def handle_cancel_payment_event(
    message: CancelPaymentEventSchema,
    payment_service: PaymentService = Depends(get_payment_service),
):
    await payment_service.cancel_payment(message.payment_id)
