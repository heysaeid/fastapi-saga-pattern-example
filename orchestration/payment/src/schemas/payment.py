from pydantic import BaseModel, PositiveInt, PositiveFloat, Field
from utils.enums import PaymentStatusEnum


class CreatePaymentSchema(BaseModel):
    order_id: PositiveInt
    amount: PositiveFloat
    status: PaymentStatusEnum = Field(PaymentStatusEnum.PENDING)


class PaymentUpdateSchema(BaseModel):
    status: PaymentStatusEnum

