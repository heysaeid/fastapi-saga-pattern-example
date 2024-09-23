from typing import List, Optional
from pydantic import BaseModel, Field, PositiveFloat, PositiveInt
from utils.enum import OrderStatusEnum


class CreateOrderItem(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt = Field(lt=11)
    unit_price: PositiveFloat


class CreateOrderSchema(BaseModel):
    customer_id: PositiveInt
    status: Optional[OrderStatusEnum] = Field(default=OrderStatusEnum.PENDING)
    total_amount: PositiveFloat
    order_items: List[CreateOrderItem]


    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "order_items": [
                    {"product_id": 1, "quantity": 2, "unit_price": 1000},
                ],
                "total_amount": 1000,
            }
        }


class CreatePaymentEventSchema(BaseModel):
    order_id: int = Field(gt=0)
    amount: float = Field(gt=0)

class CancelOrderEventSchema(BaseModel):
    order_id: PositiveInt