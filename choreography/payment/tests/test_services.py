import pytest
from src.schemas.payment import CreatePaymentSchema
from src.utils.enums import PaymentStatusEnum


@pytest.mark.asyncio
async def test_create_payment(create_payment):
    creation_data = CreatePaymentSchema(
        amount=1000,
        order_id=1,
    )
    result = await create_payment(creation_data)

    assert result.amount == 1000
    assert result.order_id == 1
    assert result.status.value == PaymentStatusEnum.PENDING.value
