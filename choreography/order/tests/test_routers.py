import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_order_endpoint(client: TestClient, mock_broker_publish):
    order_items_data = [
        {"product_id": 1, "quantity": 2, "unit_price": 100.0},
        {"product_id": 2, "quantity": 1, "unit_price": 200.0},
    ]
    create_order_data = {
        "customer_id": 123,
        "total_amount": 300.0,
        "order_items": order_items_data,
        "province": "Tehran",
        "city": "Tehran",
    }

    response = client.post("/orders/create_order", json=create_order_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["customer_id"] == create_order_data["customer_id"]
    assert response_data["total_amount"] == create_order_data["total_amount"]
    assert len(response_data["order_items"]) == 2
    assert (
        response_data["order_items"][0]["product_id"]
        == order_items_data[0]["product_id"]
    )
    assert (
        response_data["order_items"][1]["product_id"]
        == order_items_data[1]["product_id"]
    )
