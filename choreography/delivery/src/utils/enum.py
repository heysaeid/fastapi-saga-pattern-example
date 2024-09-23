from enum import Enum


class DeliveryStatusEnum(Enum):
    PENDING = "Pending"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class KafkaTopicEnum(str, Enum):
    CREATE_DELIVERY = "create-delivery"
    CANCEL_PAYMENT = "cancel-payment"