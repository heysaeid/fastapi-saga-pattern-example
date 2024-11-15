from pydantic import PositiveInt
from models.payment import Payment
from repositories.payment import PaymentRepository
from schemas.payment import CreatePaymentSchema
from utils.enums import PaymentStatusEnum
from utils.exceptions import NotFoundException


class PaymentService:
    def __init__(self, payment_repo: PaymentRepository):
        self.payment_repo = payment_repo

    async def get_payment_or_404(self, payment_id: PositiveInt):
        payment = await self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise NotFoundException
        return payment

    async def create_payment(self, creation_data: CreatePaymentSchema):
        payment = await self.payment_repo.create(
            entity=Payment(**creation_data.model_dump())
        )
        return payment

    async def confirm_payment(self, payment_id: PositiveInt):
        payment = await self._update_payment_status(payment_id, PaymentStatusEnum.COMPLETED)
        return payment

    async def cancel_payment(self, payment_id: PositiveInt):
        payment = await self._update_payment_status(payment_id, PaymentStatusEnum.REFUNDED)
        return payment

    async def _update_payment_status(
        self, payment_id: PositiveInt, status: PaymentStatusEnum
    ):
        payment = await self.get_payment_or_404(payment_id)
        payment = await self.payment_repo.update(payment, status=status)
        return payment
