from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.order import OrderRepository
from services.order import OrderService
from database import get_session
from services.order_process import OrderProcessService


async def get_order_repository(db: AsyncSession = Depends(get_session)):
    return OrderRepository(db)

async def get_order_service(
    order_repo: OrderRepository = Depends(get_order_repository)
):
    return OrderService(order_repo)

async def get_order_process_service(
    order_service: OrderService = Depends(get_order_service)
):
    return OrderProcessService(order_service)