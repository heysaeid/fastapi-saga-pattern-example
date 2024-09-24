from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from services.payment import PaymentService
from utils.dependencies import get_payment_service


router = APIRouter()


@router.post("/{payment_id}/confirm")
async def confirm_payment(
    payment_id: PositiveInt, 
    payment_service: PaymentService = Depends(get_payment_service),
):
    payment = await payment_service.confirm_payment(payment_id)
    return {"message": "Payment confirmed", "payment": payment}

@router.post("/{payment_id}/cancel")
async def cancel_payment(
    payment_id: PositiveInt, 
    payment_service: PaymentService = Depends(get_payment_service),
):
    payment = await payment_service.cancel_payment(payment_id)
    return {"message": "Payment canceled", "payment": payment}