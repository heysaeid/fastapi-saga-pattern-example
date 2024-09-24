from faststream import Depends
from stream import broker
from database import get_session
from repositories.delivery import DeliveryRepository
from repositories.delivery_person import DeliveryPersonRepository
from services.delivery import DeliveryService
from schemas.delivery import CreateDeliveryEventSchema
from utils.enums import KafkaTopicEnum


def get_delivery_service(db = Depends(get_session)):
    delivery_repo = DeliveryRepository(db)
    delivery_person_repo = DeliveryPersonRepository(db)
    return DeliveryService(delivery_repo, delivery_person_repo)


@broker.subscriber(KafkaTopicEnum.CREATE_DELIVERY, group_id=f"grp-{KafkaTopicEnum.CREATE_DELIVERY}")
async def handle_create_delivery_event(
    message: CreateDeliveryEventSchema,
    delivery_service: DeliveryService = Depends(get_delivery_service),
) -> None:
    await delivery_service.create_delivery(message)