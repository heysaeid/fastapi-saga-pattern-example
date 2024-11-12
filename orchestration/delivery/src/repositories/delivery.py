from models.delivery import Delivery
from repositories.base import BaseRepository


class DeliveryRepository(BaseRepository[Delivery]):
    model_class = Delivery
