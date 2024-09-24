from models.delivery import DeliveryPerson
from repositories.base import BaseRepository


class DeliveryPersonRepository(BaseRepository[DeliveryPerson]):
    model_class = DeliveryPerson

    async def get_by_location(self, province: str, city: str):
        query = self._select().filter_by(province=province, city=city)
        query = await self.session.scalars(query)
        return query.first()
