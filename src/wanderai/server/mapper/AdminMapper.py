from sqlalchemy import delete, select

from wanderai.common.context import BaseContext
from wanderai.model.entity import Admin, User
from wanderai.model.schema import AdminModel, SuggestionModel, UserHistoryModel, UserModel


async def list_users() -> list[User]:
    """列出所有用户"""
    db = BaseContext.get_db_session()
    stmt = select(UserModel)
    result = await db.execute(stmt)
    results = result.scalars().all()
    return [User.model_validate(user) for user in results]


async def get_account(account_id: str) -> User:
    """查找具体用户"""
    db = BaseContext.get_db_session()
    stmt = select(UserModel).where(UserModel.account_id == account_id)
    result = await db.execute(stmt)
    dmin_model = result.scalar_one_or_none()
    return User.model_validate(dmin_model)


async def get_admin_by_admin_id(admin_id: str) -> Admin | None:
    """通过管理员ID获取管理员"""
    db = BaseContext.get_db_session()
    stmt = select(AdminModel).where(AdminModel.admin_id == admin_id)
    result = await db.execute(stmt)
    Admin_model = result.scalar_one_or_none()
    return Admin.model_validate(Admin_model) if Admin_model else None


async def delete_account(account_id: str):
    """注销账户"""
    db = BaseContext.get_db_session()
    stmt = delete(UserModel).where(UserModel.account_id == account_id)
    await db.execute(stmt)
    stmt = delete(SuggestionModel).where(SuggestionModel.account_id == account_id)
    await db.execute(stmt)
    stmt = delete(UserHistoryModel).where(UserHistoryModel.account_id == account_id)
    await db.execute(stmt)
