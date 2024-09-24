from pydantic import PositiveInt
from fastapi.exceptions import HTTPException
from models.payment import Payment
from repositories.payment import PaymentRepository
from schemas.payment import CreatePaymentSchema, ConfirmedOrderEventSchema, CancelOrderEventSchema
from utils.enums import PaymentStatusEnum, KafkaTopicEnum
from stream import broker



class PaymentService:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo

    async def get_payment_or_404(self, payment_id: PositiveInt):
        payment = await self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail=f"Payment with id {payment_id} not found.")
        return payment

    async def create_payment(self, creation_data: CreatePaymentSchema):
        payment = await self.payment_repo.create(
            entity=Payment(**creation_data.model_dump()),
            commit=True,
        )
        return payment

    async def confirm_payment(self, payment_id: PositiveInt):
        payment = await self.get_payment_or_404(payment_id)
        payment.status = PaymentStatusEnum.COMPLETED
        await self.payment_repo.update(payment, commit=True)
        await broker.publish(
            topic=KafkaTopicEnum.CONFIRMED_ORDER,
            message=ConfirmedOrderEventSchema(order_id=payment.order_id),
        )
        return payment

    async def cancel_payment(self, payment_id: PositiveInt):
        payment = await self.get_payment_or_404(payment_id)
        payment.status = PaymentStatusEnum.REFUNDED
        await self.payment_repo.update(payment, commit=True)
        await broker.publish(
            topic=KafkaTopicEnum.CANCEL_ORDER,
            message=CancelOrderEventSchema(order_id=payment.order_id),
        )
        return payment