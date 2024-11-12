from typing import Annotated
from fastapi import APIRouter, Depends
from services.delivery import DeliveryService
from schemas.delivery import CreateDeliverySchema
from utils.dependencies import get_delivery_service


router = APIRouter()

@router.post(
    "/create_delivery",
    status_code=201,
    response_model=CreateDeliverySchema,
)
async def create_delivery(
    delivery_service: Annotated[DeliveryService, Depends(get_delivery_service)],
    data: CreateDeliverySchema,
):
    await delivery_service.create_delivery(data)
    return {"message": "Delivery created successfully"}
