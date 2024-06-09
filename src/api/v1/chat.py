from typing import Sequence

from fastapi import APIRouter, Depends

from schemas.chat import MessageSchema
from services.chat import ChatService
from core.oauth2_scheme import oauth2_scheme

router = APIRouter(prefix="/chat", tags=["Authentication"], dependencies=[Depends(oauth2_scheme)])


@router.post("/send_message")
async def send_message(text: str, chat_service: ChatService = Depends()) -> MessageSchema:
    return await chat_service.send_message(text=text)


@router.get("/get_messages")
async def get_messages(chat_service: ChatService = Depends()) -> Sequence[MessageSchema]:
    return await chat_service.get_messages()
