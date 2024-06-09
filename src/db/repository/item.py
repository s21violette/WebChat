from typing import Sequence

from sqlalchemy import select

from db.models.item import Item
from db.repository.base import BaseDatabaseRepository
from schemas.item import ItemSchema


class ItemRepository(BaseDatabaseRepository):
    async def get_items(self) -> Sequence[ItemSchema]:
        query = select(Item)
        result = await self._session.execute(query)
        items = result.scalars().all()

        return [ItemSchema.model_validate(item) for item in items]

    async def get_item_by_id(self, item_id: int) -> ItemSchema | None:
        query = select(Item).filter(Item.id == item_id)
        result = await self._session.execute(query)
        item = result.scalar_one_or_none()

        return ItemSchema.model_validate(item) if item else None
