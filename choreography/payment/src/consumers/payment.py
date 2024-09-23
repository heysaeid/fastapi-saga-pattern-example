from utils.stream import broker
from fastapi import Depends
from database import get_session
from src.repositories.payment import PaymentRepository
from src.services.payment import PaymentService
from src.utils.enum import KafkaTopicEnum
from src.schemas.payment import CreatePaymentSchema, CreatePaymentEventSchema, CancelPaymentEventSchema


def get_payment_service(db = Depends(get_session)):
    payment_repo = PaymentRepository(db)
    return PaymentService(payment_repo)


@broker.subscriber(KafkaTopicEnum.CREATE_PAYMENT, group_id=f"grp_{KafkaTopicEnum.CREATE_PAYMENT}")
async def handle_create_payment_event(
    message: CreatePaymentEventSchema,
    payment_service: PaymentService = Depends(get_payment_service),
):
    payment_data = CreatePaymentSchema(
        order_id=message["order_id"],
        amount=message["amount"],
        status=message.get("status"),
    )
    new_payment = await payment_service.create_payment(payment_data)
    print(f"New payment created: {new_payment.id}")


@broker.subscriber(KafkaTopicEnum.CANCEL_PAYMENT, group_id=f"grp_{KafkaTopicEnum.CANCEL_PAYMENT}")
async def handle_cancel_payment_event(
    message: CancelPaymentEventSchema,
    payment_service: PaymentService = Depends(get_payment_service),
):
    payment_id = message["payment_id"]
    await payment_service.cancel_payment(payment_id)
    print(f"Canceled Payment: {payment_id}")
