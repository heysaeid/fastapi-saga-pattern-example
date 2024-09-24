from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.payment import PaymentRepository
from services.payment import PaymentService
from database import get_session


def get_payment_repository(db: AsyncSession = Depends(get_session)):
    return PaymentRepository(db)

def get_payment_service(payment_repo: PaymentRepository = Depends(get_payment_repository)):
    return PaymentService(payment_repo)