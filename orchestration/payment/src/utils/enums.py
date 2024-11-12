from enum import StrEnum


class PaymentStatusEnum(StrEnum):
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"

