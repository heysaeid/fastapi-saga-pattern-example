from fastapi import APIRouter
from .order import router as order_router

api_router = APIRouter()
api_router.include_router(order_router, prefix="/orders", tags=["order"])