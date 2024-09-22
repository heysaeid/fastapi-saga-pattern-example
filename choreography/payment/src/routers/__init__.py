from fastapi import APIRouter
from .payment import router as payment_router


api_router = APIRouter()
api_router.include_router(payment_router, prefix="/payments", tags=["payment"])