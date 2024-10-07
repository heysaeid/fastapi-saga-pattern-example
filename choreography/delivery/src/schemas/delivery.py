from pydantic import BaseModel, PositiveInt


class CreateDeliverySchema(BaseModel):
    order_id: PositiveInt
    payment_id: PositiveInt
    province: str
    city: str


class CreateDeliveryEventSchema(CreateDeliverySchema):
    ...


class CancelPaymentEventSchema(BaseModel):
    payment_id: PositiveInt


class AssignDeliveryToPersonEventSchema(BaseModel):
    delivery_id: PositiveInt
