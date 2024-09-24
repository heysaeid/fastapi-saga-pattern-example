from pydantic import BaseModel, PositiveInt


class CreateDeliverySchema(BaseModel):
    order_id: PositiveInt
    province: str
    city: str


class CreateDeliveryEventSchema(CreateDeliverySchema):
    ...


class CancelPaymentEventSchema(BaseModel):
    order_id: PositiveInt