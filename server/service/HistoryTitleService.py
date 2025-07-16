from common.context import BaseContext
from model.entity import HistoryTitle
from server.mapper import HistoryTitleMapper

async def get_history_title_by_account_id() -> list[HistoryTitle] | None:
    """获取历史标题"""
    account_id = BaseContext.get_account_id()
    if not account_id:
        raise ValueError("Account ID is Null")
    return await HistoryTitleMapper.get_history_title_by_account_id(account_id)
