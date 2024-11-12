from enum import StrEnum


class DeliveryStatusEnum(StrEnum):
    PENDING = "Pending"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
