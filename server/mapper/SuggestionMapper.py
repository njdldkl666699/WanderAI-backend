from sqlalchemy import select, delete

from common.context import BaseContext
from model.entity import Suggestion
from model.schema import SuggestionModel


async def create_suggestion(suggestion: Suggestion) -> None:
    """创建新建议"""
    db = BaseContext.get_db_session()
    suggestion_model = SuggestionModel(**suggestion.model_dump())
    db.add(suggestion_model)


async def get_suggestion(account_id: str) -> list[Suggestion]:
    """查找用户建议"""
    db = BaseContext.get_db_session()
    stmt = select(SuggestionModel).where(SuggestionModel.account_id == account_id)
    result = await db.execute(stmt)
    results = result.scalars().all()
    return [Suggestion.model_validate(suggestion) for suggestion in results]


async def get_all_suggestion() -> list[Suggestion]:
    """查找所有用户建议"""
    db = BaseContext.get_db_session()
    stmt = select(SuggestionModel)
    result = await db.execute(stmt)
    results = result.scalars().all()
    return [Suggestion.model_validate(suggestion) for suggestion in results]


async def delete_suggestion(id: int):
    """删除建议"""
    db = BaseContext.get_db_session()
    stmt = delete(SuggestionModel).where(SuggestionModel.id == id)
    await db.execute(stmt)
