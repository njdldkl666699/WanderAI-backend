from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class UserLoginVO(BaseModel):
    """用户登录VO"""
    nickname: str = Field(description="用户昵称")
    account_id: int = Field(description="用户账号ID")

class UserRegisterVO(BaseModel):
    """用户注册VO"""
    account_id: int = Field(description="用户账号ID")

class CreateSessionVO(BaseModel):
    """创建会话VO"""
    session_id: str = Field(description="会话ID")

class HistoryTitleVO(BaseModel):
    """历史会话标题VO"""
    title: str = Field(description="会话标题")
    session_id: str = Field(description="会话ID")

class HistoryMessageVO(BaseModel):
    """历史消息VO"""
    type: str = Field(description="消息类型")
    message: str = Field(description="消息内容")
