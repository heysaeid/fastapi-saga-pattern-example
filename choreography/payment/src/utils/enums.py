from enum import StrEnum


class PaymentStatusEnum(StrEnum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class KafkaTopicEnum(StrEnum):
    CREATE_PAYMENT = "create-payment"
    CONFIRM_ORDER = "confirm-order"
    CANCEL_ORDER = "cancel-order"
    CANCEL_PAYMENT = "cancel-payment"
