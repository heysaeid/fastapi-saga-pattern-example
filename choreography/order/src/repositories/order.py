from models.order import Order
from repositories.base import BaseRepository


class OrderRepository(BaseRepository):
    model_class = Order
