from schemas.base import BaseSchema


class ItemSchema(BaseSchema):
    id: int
    item_num: int
    description: str
    is_active: bool
