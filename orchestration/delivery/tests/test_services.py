import pytest
from fastapi import HTTPException
from src.services.delivery import DeliveryService
from src.schemas.delivery import CreateDeliverySchema
from src.models.delivery import DeliveryPerson
from src.services.delivery_person import DeliveryPersonService


@pytest.mark.asyncio
async def test_create_delivery_with_assign_to_person_success(
    delivery_service: DeliveryService, 
    delivery_person_repo: DeliveryPersonService, 
):
    creation_data = CreateDeliverySchema(
        order_id=1,
        payment_id=1,
        province="Tehran",
        city="Tehran",
    )
    delivery_person = DeliveryPerson(
        id=1, 
        name="Ali", 
        phone_number="09123456789", 
        province=creation_data.province, 
        city=creation_data.city,
    )
    await delivery_person_repo.create(delivery_person)
    delivery = await delivery_service.create_delivery(creation_data)
    is_assigned = await delivery_service.assign_delivery_to_person(delivery.id)
    assert is_assigned is True


@pytest.mark.asyncio
async def test_create_delivery_with_assign_to_person_fail(delivery_service: DeliveryService):
    creation_data = CreateDeliverySchema(
        order_id=1,
        payment_id=1,
        province="Tehran",
        city="Tehran",
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await delivery_service.create_delivery(creation_data)
        assert exc_info.value.args[0] == "Delivery person not available"
