from pydantic import BaseModel


class CreateDeliverySchema(BaseModel):
    order_id: int
    province: str
    city: str


class CreateDeliveryEventSchema(CreateDeliverySchema):
    ...