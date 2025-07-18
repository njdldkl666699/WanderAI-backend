from langchain_core.messages import AIMessage, HumanMessage

from common.constant.MessageConstant import MESSAGE_LIST_IS_EMPTY, PLEASE_LOGIN, SESSION_NOT_FOUND
from common.context import BaseContext
from common.exception import (
    MessageListEmptyException,
    SessionNotFoundException,
    UserNotFoundException,
)
from model.entity import UserHistory
from model.vo import HistoryListVO, HistoryMessageVO, HistoryTitleVO
from server.agent.interface import TitleGenerator, TravelChatAgent
from server.mapper import UserHistoryMapper


async def list_history() -> list[HistoryListVO]:
    """获取历史标题列表"""
    account_id = BaseContext.get_account_id()
    if not account_id:
        raise UserNotFoundException(PLEASE_LOGIN)

    user_history_list = await UserHistoryMapper.list_by_account_id(account_id)
    history_list_vos = [
        HistoryListVO(title=user_history.title, session_id=user_history.session_id)
        for user_history in user_history_list
    ]

    # 逆序返回历史列表
    history_list_vos.reverse()
    return history_list_vos


async def create_history_title(session_id: str) -> HistoryTitleVO:
    """创建新的历史标题"""
    account_id = BaseContext.get_account_id()
    if not account_id:
        raise UserNotFoundException(PLEASE_LOGIN)

    # 根据会话id获取当前历史记录
    user_history_list = await UserHistoryMapper.get_by_session_account(session_id, account_id)
    if not user_history_list:
        # 如果没有找到对应的会话id，抛出异常
        raise SessionNotFoundException(SESSION_NOT_FOUND)

    messages = None
    async for graph in TravelChatAgent.create_travel_plan_graph():
        # 获取当前会话id的所有消息
        messages = await TravelChatAgent.get_history_messages(graph, session_id)

    if not messages:
        raise MessageListEmptyException(MESSAGE_LIST_IS_EMPTY)

    # 调用AI模型生成标题
    title = TitleGenerator.generate_title(messages)

    history_db = user_history_list[0]
    history_new = UserHistory(
        id=history_db.id,
        account_id=history_db.account_id,
        session_id=session_id,
        title=title,
    )
    # 更新数据库
    await UserHistoryMapper.update_user_history(history_new)

    return HistoryTitleVO(title=title)


async def get_chat_content_by_session_id(session_id: str) -> list[HistoryMessageVO]:
    """获取历史聊天内容"""
    messages = None
    async for graph in TravelChatAgent.create_travel_plan_graph():
        messages = await TravelChatAgent.get_history_messages(graph, session_id)
    if not messages:
        raise MessageListEmptyException(MESSAGE_LIST_IS_EMPTY)

    # 将消息转换为HistoryMessageVO
    history_messages: list[HistoryMessageVO] = []
    for message in messages:
        if isinstance(message, HumanMessage) and isinstance(message.content, str):
            history_messages.append(HistoryMessageVO(type="human", message=message.content))
        if isinstance(message, AIMessage) and isinstance(message.content, str):
            history_messages.append(HistoryMessageVO(type="chat", message=message.content))
        if isinstance(message, AIMessage) and isinstance(message.content, list):
            history_messages.append(HistoryMessageVO(type="plan", message=message.content[0]))

    return history_messages
