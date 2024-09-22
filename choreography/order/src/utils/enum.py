from enum import Enum


class OrderStatusEnum(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    DISPATCHED = "Dispatched"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
