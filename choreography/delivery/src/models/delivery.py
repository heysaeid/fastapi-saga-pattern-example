from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from utils.enum import DeliveryStatusEnum
from . import Base


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False, index=True)
    delivery_person_id = Column(Integer, ForeignKey("delivery_persons.id"), nullable=False)
    delivery_person = relationship("DeliveryPerson", back_populates="deliveries")
    status = Column(Enum(DeliveryStatusEnum), default=DeliveryStatusEnum.IN_TRANSIT)
    delivery_data = Column(DateTime, nullable=True)
    estimated_time = Column(DateTime, nullable=True)
    province = Column(String, nullable=False)
    city = Column(String, nullable=False)


class DeliveryPerson(Base):
    __tablename__ = "delivery_persons"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    province = Column(String, nullable=False)
    city = Column(String, nullable=False)
    deliveries = relationship("Delivery", back_populates="delivery_person")
