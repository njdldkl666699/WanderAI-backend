from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession

db_session_context: ContextVar[AsyncSession] = ContextVar("db_session")
user_account_id_context: ContextVar[str] = ContextVar("user_account_id")


class BaseContext:
    """应用上下文管理器"""

    # 数据库会话相关
    @staticmethod
    def set_db_session(db: AsyncSession):
        db_session_context.set(db)

    @staticmethod
    def get_db_session() -> AsyncSession:
        try:
            return db_session_context.get()
        except LookupError:
            raise RuntimeError("数据库会话未初始化")

    # 用户ID相关
    @staticmethod
    def set_user_account_id(user_account_id: str):
        user_account_id_context.set(user_account_id)

    @staticmethod
    def get_user_account_id() -> str | None:
        try:
            return user_account_id_context.get()
        except LookupError:
            return None
