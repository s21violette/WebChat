from typing import Sequence

from fastapi import Depends, Request
import jwt

from core.config import settings
from db.repository.chat import ChatRepository
from schemas.chat import MessageSchema


class ChatService:
    def __init__(self, auth_repository: ChatRepository = Depends()):
        self._auth_repository = auth_repository

    async def send_message(self, text: str, request: Request):
        token = request.headers.get('Authorization').split()[1]
        username = jwt.decode(token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM])["sub"]

        await self._auth_repository.send_message(f"{username}: {text}")

    async def get_messages(self) -> Sequence[MessageSchema]:
        return await self._auth_repository.get_messages()
