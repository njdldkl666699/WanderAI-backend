from sqlalchemy import select,update

from common.context import BaseContext
from model.entity import User
from model.schema import UserModel
from common.exception import PasswordErrorException, UserNotFoundException


async def list() -> list[User]:
    db = BaseContext.get_db_session()
    stmt = select(UserModel)
    result = await db.execute(stmt)
    results = result.scalars().all()
    return [User.model_validate(user) for user in results]


async def get_user_by_account_id(account_id: str) -> User | None:
    """通过账号ID获取用户"""
    db = BaseContext.get_db_session()
    stmt = select(UserModel).where(UserModel.account_id == account_id)
    result = await db.execute(stmt)
    user_model = result.scalar_one_or_none()
    return User.model_validate(user_model) if user_model else None

async def create_user(user: User) -> None:
    """创建新用户"""
    db = BaseContext.get_db_session()
    user_model = UserModel(**user.model_dump())
    db.add(user_model)
    await db.commit()
    await db.refresh(user_model)

async def update_user_nickname(account_id: str, new_nickname: str) -> None:
    """更新用户昵称"""
    db = BaseContext.get_db_session()
    
    #查询用户是否存在
    user_model = await db.get(UserModel, account_id)
    if not user_model:
        raise UserNotFoundException(f"用户 {account_id} 不存在")
    #更新用户昵称
    stmt= update(UserModel).where(UserModel.account_id == account_id).values(nickname=new_nickname)
    await db.execute(stmt)
    await db.commit()
