from fastapi import APIRouter, Query

from wanderai.common.log import log
from wanderai.model.result import Result
from wanderai.server.service import HistoryService

router = APIRouter(prefix="/history")


@router.get("/chatList")
async def get_chat_history():
    """获取历史聊天列表"""
    log.info("获取历史聊天列表")
    historyList = await HistoryService.list_history()
    return Result.success(historyList)


@router.get("/chatTitle")
async def create_chat_title(session_id: str = Query(alias="sessionId")):
    """生成聊天标题"""
    log.info(f"生成聊天标题，会话id：{session_id}")
    historyTitleVO = await HistoryService.create_history_title(session_id)
    return Result.success(historyTitleVO)


@router.get("/chatContent")
async def get_chat_content(session_id: str = Query(alias="sessionId")):
    """获取历史对话记录"""
    log.info(f"获取聊天内容，会话id：{session_id}")
    chat_content = await HistoryService.get_chat_content_by_session_id(session_id)
    return Result.success(chat_content)
