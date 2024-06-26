from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Request

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from chat.models import Messages
from chat.schemas import MessagesModel
from database import async_session_maker, get_async_session

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        await self.add_messages_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    @staticmethod
    async def add_messages_to_database(message: str):
        async with async_session_maker() as session:
            stmt = insert(Messages).values(
                message=message
            )
            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session),
) -> List[MessagesModel]:
    query = select(Messages).order_by(Messages.id.asc())
    messages = await session.execute(query)
    return messages.scalars().all()


@router.websocket("/ws/{login}")
async def websocket_endpoint(websocket: WebSocket, login: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{login}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
