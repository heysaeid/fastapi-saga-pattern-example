from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, Float, DateTime, Enum
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from utils.enum import PaymentStatusEnum
from sqlalchemy.orm import declarative_base, sessionmaker
from . import Base


class Payment(Base):
    __tablename__ = "payments"


    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False, index=True)
    payment_date = Column(DateTime)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatusEnum), nullable=False)
    
    __table_args__ = (
        CheckConstraint('amount > 0', name='check_positive_amount'),
        {'extend_existing': True}
    )
    #payment_method_id = Column(SmallInteger, ForeignKey("payment_methods.id"), nullable=False)
    #payment_method = relationship("PaymentMethod", back_populates="payments")


""" class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    payments = relationship("Payment", back_populates="payment_method") """
