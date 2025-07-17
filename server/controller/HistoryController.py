from fastapi import APIRouter, Query
from common.log import log
from model.result import Result
from server.service import HistoryService

router = APIRouter(prefix="/history")


@router.get("/chatList")
async def get_chat_history():
    """获取历史聊天列表"""
    log.info(f"获取历史聊天列表")
    historyList = await HistoryService.get_history_title_by_account_id()
    return Result.success(historyList)


@router.get("/chatTitle")
async def create_chat_title(session_id: str = Query(alias="sessionId")):
    """获取聊天标题"""
    log.info(f"获取聊天标题，会话id：{session_id}")
    historyTitleVO = await HistoryService.create_history_title(session_id)
    return Result.success(historyTitleVO)


@router.get("/chatContent")
async def get_chat_content(session_id: str = Query(alias="sessionId")):
    log.info(f"获取聊天内容，会话id：{session_id}")
    chat_content = await HistoryService.get_history_chatContent_by_session_id(session_id)
    return Result.success(chat_content)

