from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import BaseModel
from db.models.mixins import CreatedAtMixin, IDMixin


class Message(BaseModel, IDMixin, CreatedAtMixin):
    __tablename__ = "messages"

    text: Mapped[str] = mapped_column(Text, nullable=False)
