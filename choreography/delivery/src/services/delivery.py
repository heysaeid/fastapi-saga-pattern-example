from repositories.delivery import DeliveryRepository
from repositories.delivery_person import DeliveryPersonRepository
from models.delivery import Delivery
from utils.enum import DeliveryStatusEnum
from schemas.delivery import CreateDeliverySchema


class DeliveryService:
    
    def __init__(
        self, 
        delivery_repo: DeliveryRepository, 
        delivery_person_repo: DeliveryPersonRepository
    ):
        self.delivery_repo = delivery_repo
        self.delivery_person_repo = delivery_person_repo

    async def create_delivery(self, creation_data: CreateDeliverySchema):
        delivery_person = await self.delivery_person_repo.get_by_location(
            province=creation_data.province, 
            city=creation_data.city,
        )
        
        if not delivery_person:
            
            print(f"No delivery person available for province: {creation_data.province}, city: {creation_data.city}")
            return None
        
        new_delivery = Delivery(
            order_id=creation_data.order_id,
            delivery_person_id=delivery_person.id,
            status=DeliveryStatusEnum.IN_TRANSIT.value,
            province=creation_data.province,
            city=creation_data.city,
        )
        
        await self.delivery_repo.create(new_delivery, commit=True)
        return new_delivery