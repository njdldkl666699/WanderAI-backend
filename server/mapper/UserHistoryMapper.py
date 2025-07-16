from sqlalchemy import select, update

from common.context import BaseContext
from model.entity import UserHistory
from model.schema import UserHistoryModel

async def create_user_history(userhistory: UserHistory) -> None:
    """创建新会话"""
    db = BaseContext.get_db_session()
    user_model = UserHistoryModel(**userhistory.model_dump())
    db.add(user_model)
