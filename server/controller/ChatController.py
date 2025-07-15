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
    create_session_vo = ChatService.create_session()
    return Result.success(create_session_vo)


@router.get("/models")
async def get_models():
    """获取可用的模型列表"""
    log.info("请求获取可用模型列表")
    models = ChatService.list_models()
    return Result.success(models)


@router.post("/{sessionId}")
async def chat(
    chat_message_dto: ChatMessageDTO, session_id: str = Path(..., alias="sessionId")
):
    """发送消息到指定会话"""
    log.info(f"会话ID: {session_id}, 使用模型: {chat_message_dto.model}")
    generator = ChatService.stream_chat(chat_message_dto, session_id)
    return StreamResult.create_streaming_response(generator)
