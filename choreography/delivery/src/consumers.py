from faststream import Depends, Logger
from stream import broker
from database import get_session
from repositories.delivery import DeliveryRepository
from repositories.delivery_person import DeliveryPersonRepository
from services.delivery import DeliveryService
from schemas.delivery import CreateDeliveryEventSchema
from utils.enums import KafkaTopicEnum
from services.delivery_person import DeliveryPersonService
from schemas.delivery import AssignDeliveryToPersonEventSchema


def get_delivery_service(db = Depends(get_session)):
    delivery_repo = DeliveryRepository(db)
    delivery_person_repo = DeliveryPersonRepository(db)
    delivery_person_service = DeliveryPersonService(delivery_person_repo)
    return DeliveryService(delivery_repo, delivery_person_service)


@broker.subscriber(KafkaTopicEnum.CREATE_DELIVERY, group_id=f"{KafkaTopicEnum.CREATE_DELIVERY}-grp")
async def handle_create_delivery_event(
    message: CreateDeliveryEventSchema,
    logger: Logger,
    delivery_service: DeliveryService = Depends(get_delivery_service),
) -> None:
    await delivery_service.create_delivery(message)
    logger.info(f"New delivery created: {message}")


@broker.subscriber(KafkaTopicEnum.ASSIGN_DELIVERY_TO_PERSON, group_id=f"{KafkaTopicEnum.ASSIGN_DELIVERY_TO_PERSON}-grp")
async def handle_assign_delivery_to_person_event(
    message: AssignDeliveryToPersonEventSchema,
    logger: Logger,
    delivery_service: DeliveryService = Depends(get_delivery_service),
) -> None:
    is_assigned = await delivery_service.assign_delivery_to_person(message.delivery_id)
    logger.info(f"Delivery assigned to person: {is_assigned}")