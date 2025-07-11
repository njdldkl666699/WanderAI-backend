from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Literal


class StudentDTO(BaseModel):
    ID: str
    name: str | None = None
    dept_name: str | None = None
    tot_cred: Decimal | None = None


class UserLoginDTO(BaseModel):
    name: str
    password: str


class ChatOnceDTO(BaseModel):
    message: str


class ChatMessage(BaseModel):
    role: Literal["user", "ai"]
    content: str


class ChatMessageDTO(BaseModel):
    """用户发送的最新消息"""

    message: str = Field(description="用户发送的消息内容")
    model: str = Field(description="使用的模型名称")
