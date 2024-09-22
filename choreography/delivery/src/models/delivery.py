import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base



class DeliveryStatus(PyEnum):
    PENDING = "Pending"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False, index=True)
    delivery_person_id = Column(Integer, ForeignKey("delivery_persons.id"), nullable=False)
    status = Column(Enum(DeliveryStatus), default=DeliveryStatus.IN_TRANSIT)
    delivery_data = Column(DateTime, nullable=True)
    estimated_time = Column(DateTime, nullable=True)


class DeliveryPerson(Base):
    __tablename__ = "delivery_persons"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    deliveries = relationship("Delivery", back_populates="delivery_person")
