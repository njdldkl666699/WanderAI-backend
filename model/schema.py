from sqlalchemy import INT, TEXT, VARCHAR, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    """用户模型"""

    __tablename__ = "user"

    account_id = Column(VARCHAR(10), primary_key=True)
    nickname = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(255), nullable=False)

class AdminModel(Base):
    """管理员模型"""

    __tablename__ = "admin"

    admin_id = Column(VARCHAR(10), primary_key=True)
    password = Column(VARCHAR(255), nullable=False)

class UserHistoryModel(Base):
    """用户历史会话模型"""

    __tablename__ = "user_history"

    id = Column(INT, primary_key=True, autoincrement=True)
    account_id = Column(VARCHAR(10), nullable=False)
    session_id = Column(VARCHAR(150), nullable=False)
    title = Column(VARCHAR(255))


class SuggestionModel(Base):
    """用户建议模型"""

    __tablename__ = "suggestion"

    id = Column(INT, primary_key=True, autoincrement=True,nullable=False)
    account_id = Column(VARCHAR(10), nullable=False)
    message = Column(TEXT)
