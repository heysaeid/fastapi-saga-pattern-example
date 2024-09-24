from models.order import Order
from repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    model_class = Order
