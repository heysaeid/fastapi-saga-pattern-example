from enum import Enum


class OrderStatusEnum(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    DISPATCHED = "Dispatched"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class KafkaTopicEnum(str, Enum):
    CREATE_PAYMENT = "create-payment"
    CANCEL_ORDER = "cancel-order"
