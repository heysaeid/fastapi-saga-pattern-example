from httpx import AsyncClient
from pydantic import PositiveInt
from config import settings
from services.order import OrderService
from schemas.order import (
    CreateDeliveryRequestSchema,
    CreatePaymentRequestSchema, 
    CreatePaymentResponseSchema,
)
from schemas.order import CreateOrderSchema


class OrderProcessService:

    def __init__(self, order_service: OrderService = None) -> None:
        self.order_service = order_service

    async def start_order_process(self, creation_data: CreateOrderSchema):
        order = await self.order_service.create_order(creation_data)
        is_payment_created = await self.process_payment(data=CreatePaymentRequestSchema(
            order_id=order.id,
            amount=order.amount,
        ))
        if is_payment_created:
            await self.order_service.confirm_order(order.id)
            is_delivery_created = await self.process_delivery(data=CreateDeliveryRequestSchema(
                order_id=order.id,
                province=order.province,
                city=order.city,
            ))
            if is_delivery_created:
                return
        
        await self.order_service.cancel_order(order.id)

    async def process_payment(self, data: CreatePaymentRequestSchema) -> bool:
        async with AsyncClient() as client:
            create_payment_response = await client.post(
                settings.create_payment_endpoint,
                json=data.model_dump()
            )
        if create_payment_response.status_code == 201:
            payment = CreatePaymentResponseSchema(create_payment_response.json())
            return await self.confirm_payment(payment.payment_id)
        return False

    async def confirm_payment(self, payment_id: PositiveInt) -> bool:
        async with AsyncClient() as client:
            confirm_payment_response = await client.post(
                settings.confirm_payment_endpoint,
                json={
                    "payment_id": payment_id,
                }
            )
        if confirm_payment_response.status_code == 200:
            return True
        return False

    async def cancel_payment(self, payment_id: PositiveInt) -> bool:
        async with AsyncClient() as client:
            cancel_payment_response = await client.post(
                settings.cancel_payment_endpoint,
                json={
                    "payment_id": payment_id,
                }
            )
        if cancel_payment_response.status_code == 200:
            return True
        return False

    async def process_delivery(self, data: CreateDeliveryRequestSchema) -> bool:
        async with AsyncClient() as client:
            create_delivery_response = await client.post(
                settings.create_delivery_endpoint,
                json=data.model_dump()
            )
        if create_delivery_response.status_code == 201:
            return True
        return False