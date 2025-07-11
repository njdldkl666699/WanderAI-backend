from sqlalchemy import select

from common.context import BaseContext
from model.entity import User
from model.schema import UserModel


async def get_user_by_name(name: str) -> User | None:
    db = BaseContext.get_db_session()
    stmt = select(UserModel).where(UserModel.name == name)
    result = await db.execute(stmt)
    user_model = result.scalar_one_or_none()
    return User.model_validate(user_model) if user_model else None


async def list() -> list[User]:
    db = BaseContext.get_db_session()
    stmt = select(UserModel)
    result = await db.execute(stmt)
    results = result.scalars().all()
    return [User.model_validate(user) for user in results]
