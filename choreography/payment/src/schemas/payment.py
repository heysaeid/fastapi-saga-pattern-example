from pydantic import BaseModel, PositiveInt, PositiveFloat, Field
from utils.enums import PaymentStatusEnum


class CreatePaymentSchema(BaseModel):
    order_id: PositiveInt
    amount: PositiveFloat
    status: PaymentStatusEnum = Field(PaymentStatusEnum.PENDING)


class PaymentUpdateSchema(BaseModel):
    status: PaymentStatusEnum


class CreatePaymentEventSchema(CreatePaymentSchema):
    ...


class CancelPaymentEventSchema(BaseModel):
    order_id: PositiveInt


class CancelOrderEventSchema(BaseModel):
    order_id: PositiveInt


class ConfirmOrderEventSchema(BaseModel):
    order_id: PositiveInt
