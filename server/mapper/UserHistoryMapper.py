from sqlalchemy import select

from common.context import BaseContext
from model.entity import UserHistory
from model.schema import UserHistoryModel


async def create_user_history(userhistory: UserHistory) -> None:
    """创建新会话"""
    db = BaseContext.get_db_session()
    user_model = UserHistoryModel(**userhistory.model_dump())
    db.add(user_model)


async def get_session_ids_by_account_id(account_id: str) -> list[str] | None:
    """通过用户ID获取会话ID"""
    db = BaseContext.get_db_session()
    stmt = select(UserHistoryModel.session_id).where(UserHistoryModel.account_id == account_id)
    result = await db.execute(stmt)
    session_ids = result.scalars().all()
    return list(session_ids)
