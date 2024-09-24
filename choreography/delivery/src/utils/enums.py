from enum import StrEnum


class DeliveryStatusEnum(StrEnum):
    PENDING = "Pending"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class KafkaTopicEnum(StrEnum):
    CREATE_DELIVERY = "create-delivery"
    CREATE_PAYMENT = "create-payment"
    CANCEL_PAYMENT = "cancel-payment"
