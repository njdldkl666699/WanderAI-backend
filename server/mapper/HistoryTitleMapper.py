from sqlalchemy import select

from common.context import BaseContext
from model.entity import HistoryTitle
from model.schema import HistoryTitleModel

async def create_history_title(history_title: HistoryTitle) -> None:
    """创建新的历史标题"""
    db = BaseContext.get_db_session()
    history_title_model = HistoryTitleModel(**history_title.model_dump())
    db.add(history_title_model)

async def get_history_title_by_account_id(account_id: str) -> list[HistoryTitle] | None:
    """通过用户ID获取历史标题"""
    db = BaseContext.get_db_session()
    stmt = select(HistoryTitleModel).where(HistoryTitleModel.account_id == account_id)
    result = await db.execute(stmt)
    history_title_models = result.scalars().all()
    return [HistoryTitle.model_validate(history_title_model) for history_title_model in history_title_models] if history_title_models else None