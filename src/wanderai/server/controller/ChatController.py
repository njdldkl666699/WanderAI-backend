from fastapi import APIRouter, Path

from wanderai.common.log import log
from wanderai.model.dto import ChatMessageDTO, GuideMessageDTO
from wanderai.model.result import Result, StreamResult
from wanderai.server.service import ChatService, GuideService

router = APIRouter(prefix="/chat")


@router.get("/create")
async def create_session():
    """创建一个新的会话"""
    log.info("请求创建新会话")
    create_session_vo = await ChatService.create_session()
    return Result.success(create_session_vo)


@router.post("/{sessionId}")
async def travel_plan_or_chat(
    chat_message_dto: ChatMessageDTO, session_id: str = Path(alias="sessionId")
):
    """发送消息到指定会话"""
    log.info(f"发送消息到指定会话: {session_id}")
    generator = ChatService.travel_plan_or_chat(chat_message_dto, session_id)
    return StreamResult.create_streaming_response(generator)


@router.post("/guide/{sessionId}")
async def travel_guide(
    guide_message_dto: GuideMessageDTO, session_id: str = Path(alias="sessionId")
):
    """向导游发送消息"""
    log.info(f"向导游发送消息，会话ID: {session_id}")
    generator = GuideService.travel_guide(guide_message_dto, session_id)
    return StreamResult.create_streaming_response(generator)
