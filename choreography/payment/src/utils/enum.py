from enum import Enum


class PaymentStatusEnum(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class KafkaTopicEnum(str, Enum):
    CREATE_PAYMENT = "create-payment"
    CREATE_DELIVERY = "create-delivery"
    CANCEL_ORDER = "cancel-order"
    CANCEL_PAYMENT = "cancel-payment"