from typing import Sequence

from fastapi import Depends

from db.repository.chat import ChatRepository
from schemas.chat import MessageSchema


class ChatService:
    def __init__(self, auth_repository: ChatRepository = Depends()):
        self._auth_repository = auth_repository

    async def send_message(self, text: str) -> MessageSchema:
        return await self._auth_repository.send_message(text)

    async def get_messages(self) -> Sequence[MessageSchema]:
        return await self._auth_repository.get_messages()
