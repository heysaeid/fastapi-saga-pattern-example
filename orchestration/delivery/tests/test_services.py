import pytest
from src.services.delivery import DeliveryService
from src.schemas.delivery import CreateDeliverySchema
from src.utils.enums import DeliveryStatusEnum
from src.models.delivery import DeliveryPerson
from src.services.delivery_person import DeliveryPersonService


@pytest.mark.asyncio
async def test_create_delivery(
    delivery_service: DeliveryService, 
    mock_broker_publish,
):
    creation_data = CreateDeliverySchema(
        order_id=1,
        payment_id=1,
        province="Tehran",
        city="Tehran",
    )
    delivery = await delivery_service.create_delivery(creation_data)

    assert delivery is not None
    assert delivery.order_id == creation_data.order_id
    assert delivery.delivery_person_id is None
    assert delivery.province == creation_data.province
    assert delivery.city == creation_data.city
    assert delivery.status == DeliveryStatusEnum.PENDING
    mock_broker_publish.assert_called()


@pytest.mark.asyncio
async def test_assign_delivery_to_person_success(
    delivery_service: DeliveryService, 
    delivery_person_repo: DeliveryPersonService, 
    mock_broker_publish
):
    creation_data = CreateDeliverySchema(
        order_id=1,
        payment_id=1,
        province="Tehran",
        city="Tehran",
    )
    delivery = await delivery_service.create_delivery(creation_data)
    delivery_person = DeliveryPerson(
        id=1, 
        name="Ali", 
        phone_number="09123456789", 
        province=creation_data.province, 
        city=creation_data.city,
    )
    await delivery_person_repo.create(delivery_person)
    is_assigned = await delivery_service.assign_delivery_to_person(delivery.id)
    assert is_assigned is True
