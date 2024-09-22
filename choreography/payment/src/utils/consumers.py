import database
from utils.stream import broker
from payment.src.services.payment import PaymentService
from payment.src.repositories.payment import PaymentRepository
from database import get_session
from payment.src.schemas.payment import CreatePaymentSchema


@broker.subscriber("create-payment")
async def create_payment(data: dict) -> str:
    payment_service = PaymentService(PaymentRepository(get_session()))
    payment = await payment_service.create_payment(creation_data=CreatePaymentSchema(**data))
    print(f"Payment Created {payment.id}")