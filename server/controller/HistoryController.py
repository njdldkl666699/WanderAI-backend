from fastapi import APIRouter
from common.log import log
from model.result import Result
from server.service import HistoryTitleService

router = APIRouter(prefix="/history")


@router.get("/chatList")
async def get_chat_history():
    """获取历史聊天标题"""
    log.info(f"获取历史聊天标题")
    history = await HistoryTitleService.get_history_title_by_account_id()
    return Result.success(history)

@router.get("/chatTitle")
async def create_chat_title(title: str):
    """创建新的聊天标题"""
    log.info(f"创建新的聊天标题: {title}")
    history_title = await HistoryTitleService.create_history_title(title)
    return Result.success(history_title)
