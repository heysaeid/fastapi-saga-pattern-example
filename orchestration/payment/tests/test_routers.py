import pytest
from src.schemas.payment import CreatePaymentSchema


@pytest.mark.asyncio
async def test_confirm_payment(client, create_payment):
    await create_payment(CreatePaymentSchema(order_id=1, amount=1000))
    response = client.post("/payments/1/confirm")
    assert response.status_code == 200
    assert response.json()["message"] == "Payment confirmed"

@pytest.mark.asyncio
async def test_cancel_payment(client, create_payment):
    await create_payment(CreatePaymentSchema(order_id=1, amount=1000))
    response = client.post("/payments/1/cancel")
    assert response.status_code == 200
    assert response.json()["message"] == "Payment canceled"
