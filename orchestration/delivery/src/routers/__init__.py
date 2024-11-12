from fastapi import APIRouter
from .delivery import router as delivery_router


api_router = APIRouter()
api_router.include_router(delivery_router, prefix="/deliveries", tags=["delivery"])