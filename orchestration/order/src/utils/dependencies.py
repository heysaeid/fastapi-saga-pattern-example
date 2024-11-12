from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.order import OrderRepository
from services.order import OrderService
from database import get_session


async def get_order_repository(db: AsyncSession = Depends(get_session)):
    return OrderRepository(db)

async def get_order_service(order_repo: OrderRepository = Depends(get_order_repository)):
    return OrderService(order_repo)
