import pytest
from src.models.delivery import Delivery, DeliveryPerson
from src.services.delivery import DeliveryService
from src.repositories.delivery import DeliveryRepository
from src.repositories.delivery_person import DeliveryPersonRepository
from src.schemas.delivery import CreateDeliverySchema
from src.utils.enum import DeliveryStatusEnum
from src.repositories.delivery_person import DeliveryPersonRepository


@pytest.mark.asyncio
async def test_create_delivery_success(
    delivery_service: DeliveryService, 
    delivery_person_repo: DeliveryPersonRepository
):
    creation_data = CreateDeliverySchema(
        order_id=1,
        province="Tehran",
        city="Tehran",
    )
    delivery_person = DeliveryPerson(
        id=1, 
        name="Ali", 
        phone_number="09123456789", 
        province=creation_data.province, 
        city=creation_data.city
    )
    await delivery_person_repo.create(delivery_person, commit=True)
    delivery = await delivery_service.create_delivery(creation_data)

    assert delivery is not None
    assert delivery.order_id == creation_data.order_id
    assert delivery.delivery_person_id == delivery_person.id
    assert delivery.province == creation_data.province
    assert delivery.city == creation_data.city
    assert delivery.status == DeliveryStatusEnum.IN_TRANSIT.value


@pytest.mark.asyncio
async def test_create_delivery_no_delivery_person(
    delivery_service: DeliveryService, 
):
    creation_data = CreateDeliverySchema(
        order_id=1,
        province="Tehran",
        city="Tehran",
    )
    delivery = await delivery_service.create_delivery(creation_data)
    assert delivery is None
