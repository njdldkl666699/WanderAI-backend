from fastapi import APIRouter
from common.log import log
from model.result import Result
from server.service import HistoryTitleService

router = APIRouter(prefix="/history")


@router.get("/chatList")
async def get_chat_history():
    """获取用户历史记录"""
    log.info(f"获取用户历史记录")
    history = await HistoryTitleService.get_history_title_by_account_id()
    return Result.success(history)

