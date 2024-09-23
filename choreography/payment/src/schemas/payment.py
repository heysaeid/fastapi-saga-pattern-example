from pydantic import BaseModel, Field
from utils.enum import PaymentStatusEnum


class CreatePaymentSchema(BaseModel):
    order_id: int = Field(gt=0)
    amount: float = Field(0, gt=0)
    status: PaymentStatusEnum = Field(PaymentStatusEnum.PENDING)


class PaymentUpdateSchema(BaseModel):
    status: PaymentStatusEnum


class CreatePaymentEventSchema(CreatePaymentSchema):
    ...


class CancelPaymentEventSchema(BaseModel):
    payment_id: int


class CancelOrderEventSchema(BaseModel):
    order_id: int


class CreateDeliveryEventSchema(BaseModel):
    order_id: int
    address: str