from sqlalchemy import select, update

from common.context import BaseContext
from model.entity import UserHistory
from model.schema import UserHistoryModel


async def create_user_history(user_history: UserHistory) -> None:
    """将用户历史插入数据库表"""
    db = BaseContext.get_db_session()
    user_model = UserHistoryModel(**user_history.model_dump())
    db.add(user_model)


async def update_user_history(user_history: UserHistory) -> None:
    """更新用户历史"""
    db = BaseContext.get_db_session()
    stmt = (
        update(UserHistoryModel)
        .where(UserHistoryModel.session_id == user_history.session_id)
        .values(
            id=user_history.id,
            account_id=user_history.account_id,
            title=user_history.title,
        )
    )
    await db.execute(stmt)


async def list_by_account_id(account_id: str) -> list[UserHistory]:
    """通过用户ID获取历史记录列表"""
    db = BaseContext.get_db_session()
    stmt = select(UserHistoryModel).where(UserHistoryModel.account_id == account_id)
    result = await db.execute(stmt)
    user_history_models = result.scalars().all()
    return [
        UserHistory.model_validate(user_history_model) for user_history_model in user_history_models
    ]


async def get_by_session_account(session_id: str, account_id: str) -> list[UserHistory]:
    """通过会话id获取用户历史记录"""
    db = BaseContext.get_db_session()
    stmt = select(UserHistoryModel).where(
        UserHistoryModel.session_id == session_id and UserHistoryModel.account_id == account_id
    )
    result = await db.execute(stmt)
    session_history_list = result.scalars().all()
    return list(session_history_list)
