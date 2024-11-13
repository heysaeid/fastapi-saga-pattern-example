from enum import StrEnum


class OrderStatusEnum(StrEnum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    DISPATCHED = "Dispatched"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
