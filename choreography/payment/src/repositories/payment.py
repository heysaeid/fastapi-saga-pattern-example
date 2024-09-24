from models.payment import Payment
from repositories.base import BaseRepository


class PaymentRepository(BaseRepository[Payment]):
    model_class = Payment