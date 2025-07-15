from sqlalchemy import DATETIME, INT, VARCHAR, Column, Null,TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    """用户模型"""
    __tablename__ = "user"

    account_id = Column(VARCHAR(20), primary_key=True, autoincrement=True)
    nickname = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(15), default=Null)

class UserHistoryModel(Base):
    """某个用户历史会话模型"""
    __tablename__ = "user_history"

    account_id = Column(VARCHAR(20), primary_key=True, autoincrement=True)
    session_id = Column(TEXT, nullable=False)

class HistoryTitleModel(Base):
    """历史会话列表模型"""
    __tablename__ = "history_title"

    id = Column(INT, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=False)
    session_id = Column(TEXT, nullable=False)

class MessageStoreModel(Base):
    """历史消息存储模型"""
    __tablename__ = "message_store"

    id = Column(INT, primary_key=True, autoincrement=True)
    session_id = Column(TEXT, nullable=False)
    message = Column(TEXT, nullable=False)

class SuggestionModel(Base):
    """用户建议模型"""
    __tablename__ = "suggestion"

    id = Column(INT, primary_key=True, autoincrement=True)
    account_id = Column(VARCHAR(20), nullable=False)
    message = Column(TEXT, nullable=False)
