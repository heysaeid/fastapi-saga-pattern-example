from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from services.payment import PaymentService
from utils.dependencies import get_payment_service
from schemas.payment import CreatePaymentSchema


router = APIRouter()


@router.post(
    "/create_payment",
    status_code=201,
    response_model=CreatePaymentSchema,
)
async def create_payment(
    payment_service: Annotated[PaymentService, Depends(get_payment_service)],
    data: CreatePaymentSchema
):
    payment = await payment_service.create_payment(data)
    return payment


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
