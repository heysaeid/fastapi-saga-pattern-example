from pydantic import PositiveInt
from models.delivery import Delivery
from repositories.delivery import DeliveryRepository
from schemas.delivery import CreateDeliverySchema, CancelPaymentEventSchema
from utils.enums import DeliveryStatusEnum, KafkaTopicEnum
from stream import broker
from services.delivery_person import DeliveryPersonService
from schemas.delivery import AssignDeliveryToPersonEventSchema


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
        await self.delivery_repo.create(delivery)
        await broker.publish(
            topic=KafkaTopicEnum.ASSIGN_DELIVERY_TO_PERSON,
            message=AssignDeliveryToPersonEventSchema(delivery_id=delivery.id),
        )
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
            await broker.publish(
                topic=KafkaTopicEnum.CANCEL_PAYMENT,
                message=CancelPaymentEventSchema(payment_id=delivery.payment_id),
            )
            print(f"No delivery person available for province: {delivery.province}, city: {delivery.city}")
            return False