from enum import StrEnum


class PaymentStatusEnum(StrEnum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class KafkaTopicEnum(StrEnum):
    CREATE_PAYMENT = "create-payment"
    CANCEL_ORDER = "cancel-order"
    CONFIRMED_ORDER = "confirmed-order"
    CANCEL_PAYMENT = "cancel-payment"
