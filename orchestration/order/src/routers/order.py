from typing import Annotated
from fastapi import APIRouter, status, Depends
from utils.dependencies import get_order_process_service
from schemas.order import CreateOrderSchema
from services.order_process import OrderProcessService

router = APIRouter()


@router.post(
    "/create_order",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateOrderSchema,
)
async def create_order(
    order_process_service: Annotated[OrderProcessService, Depends(get_order_process_service)],
    data: CreateOrderSchema,
):
    order = await order_process_service.start_order_process(creation_data=data)
    return order
