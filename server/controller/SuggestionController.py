from fastapi import APIRouter
from model.dto import ChatMessageDTO
from common.log import log
from model.result import Result
from server.service import SuggestionService

router = APIRouter()


@router.post("/suggestion")
async def create_suggestion(chat_message: ChatMessageDTO):
    """提交用户建议"""
    log.info(f"提交用户建议: {chat_message.message}")
    suggestion = await SuggestionService.create_suggestion(chat_message)

    return Result.success(suggestion)

