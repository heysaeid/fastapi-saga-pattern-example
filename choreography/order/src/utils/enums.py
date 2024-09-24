from enum import StrEnum


class OrderStatusEnum(StrEnum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    DISPATCHED = "Dispatched"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class KafkaTopicEnum(StrEnum):
    CREATE_PAYMENT = "create-payment"
    CONFIRMED_ORDER = "confirmed-order"
    CANCEL_ORDER = "cancel-order"
    CREATED_DELIVERY = "create-delivery"
