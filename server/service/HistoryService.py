from common.constant.MessageConstant import MESSAGE_LIST_IS_EMPTY, PLEASE_LOGIN, SESSION_NOT_FOUND
from common.context import BaseContext
from common.exception import (
    MessageListEmptyException,
    SessionNotFoundException,
    UserNotFoundException,
)
from model.entity import HistoryTitle
from model.vo import HistoryTitleVO
from server.agent.interface import TitleGenerator, TravelChatAgent
from server.mapper import HistoryTitleMapper, UserHistoryMapper


async def get_history_title_by_account_id() -> list[HistoryTitle] | None:
    """获取历史标题列表"""
    account_id = BaseContext.get_account_id()
    if not account_id:
        raise UserNotFoundException(PLEASE_LOGIN)

    # 获取当前用户的历史会话id
    user_sessions = await UserHistoryMapper.get_session_ids_by_account_id(account_id)
    if not user_sessions:
        return []

    return await HistoryTitleMapper.get_titles_by_session_ids(user_sessions)


async def create_history_title(session_id: str) -> HistoryTitleVO:
    """创建新的历史标题"""
    account_id = BaseContext.get_account_id()
    if not account_id:
        raise UserNotFoundException(PLEASE_LOGIN)

    # 获取当前用户的历史会话id
    user_sessions = await UserHistoryMapper.get_session_ids_by_account_id(account_id)
    if not user_sessions or session_id not in user_sessions:
        raise SessionNotFoundException(SESSION_NOT_FOUND)

    messages = None
    async for graph in TravelChatAgent.create_travel_plan_graph():
        # 获取当前会话id的所有消息
        messages = await TravelChatAgent.get_history_messages(graph, session_id)

    if not messages:
        raise MessageListEmptyException(MESSAGE_LIST_IS_EMPTY)

    # 调用AI模型生成标题
    title = TitleGenerator.generate_title(messages)

    # 插入到数据库
    history_title = HistoryTitle(
        id=None,
        session_id=session_id,
        title=title,
    )
    await HistoryTitleMapper.insert_history_title(history_title)

    return HistoryTitleVO(title=title)
