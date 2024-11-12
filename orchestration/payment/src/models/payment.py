from sqlalchemy import Column, Integer, Float, DateTime, Enum
from utils.enums import PaymentStatusEnum
from . import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False, index=True)
    payment_date = Column(DateTime)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatusEnum), nullable=False)
