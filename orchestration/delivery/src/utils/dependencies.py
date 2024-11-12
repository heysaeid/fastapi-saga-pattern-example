from faststream import Depends
from database import get_session
from repositories.delivery import DeliveryRepository
from repositories.delivery_person import DeliveryPersonRepository
from services.delivery import DeliveryService
from services.delivery_person import DeliveryPersonService


def get_delivery_service(db = Depends(get_session)):
    delivery_repo = DeliveryRepository(db)
    delivery_person_repo = DeliveryPersonRepository(db)
    delivery_person_service = DeliveryPersonService(delivery_person_repo)
    return DeliveryService(delivery_repo, delivery_person_service)