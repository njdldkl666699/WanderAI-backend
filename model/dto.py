from pydantic import BaseModel, Field
from typing import Literal


class UserRegisterDTO(BaseModel):
    """用户注册DTO"""

    nickname: str = Field(description="用户昵称")
    password: str = Field(description="用户密码")


class UserLoginDTO(BaseModel):
    """用户登录DTO"""

    account_id: str = Field(description="用户名", alias="accountId")
    password: str = Field(description="用户密码")


class ChatMessageDTO(BaseModel):
    """用户发送的最新消息"""

    message: str = Field(description="用户发送的消息内容")
