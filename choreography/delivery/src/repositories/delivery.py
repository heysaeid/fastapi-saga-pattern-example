from models.delivery import Delivery
from repositories.base import BaseRepository


class DeliveryRepository(BaseRepository):
    model_class = Delivery
