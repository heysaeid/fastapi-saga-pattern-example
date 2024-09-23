import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    SmallInteger,
)
from sqlalchemy.orm import relationship
from utils.enum import OrderStatusEnum
from . import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, index=True)
    order_date = Column(DateTime, default=datetime.datetime.now)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING, nullable=False)
    total_amount = Column(Float, nullable=False)

    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id", ), nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(SmallInteger, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="order_items")
