from typing import List, Optional
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt
from utils.enums import OrderStatusEnum


class CreateOrderItem(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt = Field(lt=11)
    unit_price: PositiveFloat


class CreateOrderSchema(BaseModel):
    customer_id: PositiveInt
    status: Optional[OrderStatusEnum] = Field(default=OrderStatusEnum.PENDING)
    total_amount: PositiveFloat
    order_items: List[CreateOrderItem]
    province: str = Field(max_length=80)
    city: str = Field(max_length=80)

    model_config = {
        "json_schema_extra": {
            "example": {
                "customer_id": 1,
                "order_items": [
                    {"product_id": 1, "quantity": 2, "unit_price": 1000},
                ],
                "total_amount": 1000,
                "province": "Tehran",
                "city": "Tehran",
            }
        }
    }


class CreatePaymentEventSchema(BaseModel):
    order_id: PositiveInt = Field(gt=0)
    amount: PositiveFloat = Field(gt=0)


class CreateDeliveryEventSchema(BaseModel):
    order_id: PositiveInt
    province: str
    city: str


class CancelOrderEventSchema(BaseModel):
    order_id: PositiveInt
