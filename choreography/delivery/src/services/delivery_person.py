from repositories.delivery_person import DeliveryPersonRepository


class DeliveryPersonService:
    
    def __init__(self, delivery_person_repo: DeliveryPersonRepository):
        self.delivery_person_repo = delivery_person_repo

    async def get_assignable_delivery_person(self, province, city):
        return await self.delivery_person_repo.get_by_location(province, city)
