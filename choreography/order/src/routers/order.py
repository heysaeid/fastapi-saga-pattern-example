from typing import Annotated
from fastapi import APIRouter, Depends, status
from order.src.services.order import OrderService
from database import get_session
from repositories.order import OrderRepository
from schemas.order import CreateOrderSchema

router = APIRouter()

@router.post("/create_order", status_code=status.HTTP_201_CREATED, response_model=CreateOrderSchema)
async def create_order(
    order_service: Annotated[OrderService, Depends(OrderService)],
    data: CreateOrderSchema,
    db_session = Depends(get_session),
):
    order = await order_service.create_order(
        order_repo = OrderRepository(db_session),
        creation_data = data,
    )
    return order
