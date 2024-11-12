from typing import Annotated
from fastapi import APIRouter, status, Depends
from services.order import OrderService
from utils.dependencies import get_order_service
from schemas.order import CreateOrderSchema

router = APIRouter()


@router.post(
    "/create_order",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateOrderSchema,
)
async def create_order(
    order_service: Annotated[OrderService, Depends(get_order_service)],
    data: CreateOrderSchema,
):
    order = await order_service.create_order(creation_data=data)
    return order
