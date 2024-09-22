from repositories.base import BaseRepository
from models.payment import Payment



class PaymentRepository(BaseRepository):
    model_class = Payment