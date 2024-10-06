from enum import StrEnum


class OrderStatusEnum(StrEnum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    DISPATCHED = "Dispatched"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class KafkaTopicEnum(StrEnum):
    CREATE_PAYMENT = "create-payment"
    CREATED_DELIVERY = "create-delivery"
    CONFIRM_ORDER = "confirm-order"
    CANCEL_ORDER = "cancel-order"
    CONFIRM_ORDER_DELIVERY = "confirm-order-delivery"
