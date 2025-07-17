from fastapi import Path

from common.log import log
from model.dto import ChatMessageDTO
from model.result import Result, StreamResult
from server import app
from server.service import ChatService

router = app.APIRouter(prefix="/chat")


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
    log.info(f"会话ID: {session_id}")
    # session_id_exists = await ChatService.check_session_id(session_id)
    # if not session_id_exists:
    #     log.warning("")
    #     return StreamResult.create_streaming_response(create_error_streaming_result())
    generator = ChatService.travel_plan_or_chat(chat_message_dto, session_id)
    return StreamResult.create_streaming_response(generator)


async def create_error_streaming_result():
    result = StreamResult.error("会话不存在")
    yield result.to_sse_format()
