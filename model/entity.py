from datetime import datetime
from pydantic import BaseModel, SecretStr, Field


class User(BaseModel):
    """用户模型"""
    account_id: str = Field(description="用户账号ID")
    nickname: str = Field(description="用户昵称")
    password: str = Field(description="用户密码")

    class Config:
        from_attributes = True  # 允许从ORM对象创建

class UserHistory(BaseModel):
    """某个用户历史会话模型"""
    account_id: str = Field(description="用户账号ID")
    session_id: str = Field(description="会话ID")

    class Config:
        from_attributes = True  # 允许从ORM对象创建

class HistoryTitle(BaseModel):
    """历史会话列表模型"""
    id: int = Field(description="会话ID(单纯作为主键)")
    title: str = Field(description="会话标题")
    session_id: str = Field(description="会话ID")

    class Config:
        from_attributes = True  # 允许从ORM对象创建

class Suggestion(BaseModel):
    """用户建议模型"""
    id: int = Field(description="建议ID(单纯作为主键)")
    account_id: str = Field(description="用户账号ID")
    message: str = Field(description="建议内容")

    class Config:
        from_attributes = True  # 允许从ORM对象创建

class ChatModelEntity(BaseModel):
    model: str
    temperature: float = 0.7
    base_url: str
    api_key: SecretStr
    max_tokens: int | None = None
