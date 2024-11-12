from pydantic import PositiveInt
from fastapi import HTTPException
from models.delivery import Delivery
from repositories.delivery import DeliveryRepository
from schemas.delivery import CreateDeliverySchema
from utils.enums import DeliveryStatusEnum
from services.delivery_person import DeliveryPersonService


class DeliveryService:
    
    def __init__(
        self, 
        delivery_repo: DeliveryRepository, 
        delivery_person_service: DeliveryPersonService,
    ):
        self.delivery_repo = delivery_repo
        self.delivery_person_service = delivery_person_service

    async def create_delivery(self, creation_data: CreateDeliverySchema):
        delivery = Delivery(
            status = DeliveryStatusEnum.PENDING,
            **creation_data.model_dump(),
        )
        delivery = await self.delivery_repo.create(delivery, commit=False)
        is_assigned = await self.assign_delivery_to_person(delivery.id)
        if is_assigned:
            await self.delivery_repo.commit()
        else:
            raise HTTPException(status_code=400, detail="Delivery person not available")
        return delivery

    async def assign_delivery_to_person(self, delivery_id: PositiveInt) -> bool:
        delivery = await self.delivery_repo.get_by_id(delivery_id)
        delivery_person = await self.delivery_person_service.get_assignable_delivery_person(
            province=delivery.province, city=delivery.city
        )
        if delivery_person:
            await self.delivery_repo.update(
                delivery,
                status=DeliveryStatusEnum.IN_TRANSIT, 
                delivery_person_id=delivery_person.id,
            )
            return True
        else:
            return False