from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession

db_session_context: ContextVar[AsyncSession] = ContextVar("db_session")
account_id_context: ContextVar[str] = ContextVar("account_id")
admin_id_context: ContextVar[str] = ContextVar("admin_id")


class BaseContext:
    """应用上下文管理器"""

    # 数据库会话
    @staticmethod
    def set_db_session(db: AsyncSession):
        db_session_context.set(db)

    @staticmethod
    def get_db_session() -> AsyncSession:
        try:
            return db_session_context.get()
        except LookupError:
            raise RuntimeError("数据库会话未初始化")

    # 用户ID
    @staticmethod
    def set_account_id(account_id: str):
        account_id_context.set(account_id)

    @staticmethod
    def get_account_id() -> str | None:
        try:
            return account_id_context.get()
        except LookupError:
            return None

    # 管理员id
    @staticmethod
    def set_admin_id(admin_id: str):
        admin_id_context.set(admin_id)

    @staticmethod
    def get_admin_id():
        try:
            return admin_id_context.get()
        except LookupError:
            return None
