from stream import broker
from fastapi import Depends
from database import get_session
from src.utils.enum import KafkaTopicEnum
from src.repositories.delivery_person import DeliveryPersonRepository
from src.repositories.delivery import DeliveryRepository
from src.services.delivery import DeliveryService
from src.schemas.delivery import CreateDeliveryEventSchema, CreateDeliverySchema


def get_delivery_service(db = Depends(get_session)):
    delivery_repo = DeliveryRepository(db)
    delivery_person_repo = DeliveryPersonRepository(db)
    return DeliveryService(delivery_repo, delivery_person_repo)


@broker.subscriber(KafkaTopicEnum.CREATE_DELIVERY, group_id=f"grp_{KafkaTopicEnum.CREATE_DELIVERY}")
async def handle_create_delivery_event(
    message: CreateDeliveryEventSchema,
    delivery_service: DeliveryService = Depends(get_delivery_service),
):
    payment_data = CreateDeliverySchema(
        order_id=message["order_id"],
        province=message["province"],
        city=message["city"],
    )
    new_delivery = await delivery_service.create_delivery(payment_data)
    print(f"New delivery created: {new_delivery.id}")
