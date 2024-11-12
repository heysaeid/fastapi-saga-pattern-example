from pydantic import BaseModel, PositiveInt


class CreateDeliverySchema(BaseModel):
    order_id: PositiveInt
    payment_id: PositiveInt
    province: str
    city: str
