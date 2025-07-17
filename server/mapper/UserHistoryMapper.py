from sqlalchemy import select, update

from common.context import BaseContext
from model.entity import UserHistory
from model.schema import UserHistoryModel

async def create_user_history(userhistory: UserHistory) -> None:
    """创建新会话"""
    db = BaseContext.get_db_session()
    user_model = UserHistoryModel(**userhistory.model_dump())
    db.add(user_model)

async def get_session_id_by_account_id(account_id: str) -> list[str] | None:
    """通过用户ID获取会话ID"""
    db = BaseContext.get_db_session()
    stmt = select(UserHistoryModel).where(UserHistoryModel.account_id == account_id)
    result = await db.execute(stmt)
    user_history_models = result.scalars().all()
    session_ids = [row[0] for row in user_history_models]
    return [item for row in session_ids for item in row] if session_ids else None
