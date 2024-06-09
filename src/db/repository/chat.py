from typing import Sequence

from sqlalchemy import select, insert

from core.exceptions import lost_connection_exception
from db.repository.base import BaseDatabaseRepository
from db.models.chat import Message
from schemas.chat import MessageSchema


class ChatRepository(BaseDatabaseRepository):
    async def get_messages(self) -> Sequence[MessageSchema]:
        try:
            query = select(Message.text)
            select_result = await self._session.execute(query)
            messages_list = select_result.scalars().all()
        except ConnectionRefusedError:
            raise lost_connection_exception

        return [MessageSchema(text=message) for message in messages_list]

    async def send_message(self, text: str) -> MessageSchema:
        try:
            query = insert(Message).values(text=text)
            await self._session.execute(query)
            await self._session.commit()
        except ConnectionRefusedError:
            raise lost_connection_exception

        return MessageSchema(text=text)
