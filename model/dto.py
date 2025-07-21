from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class UserRegisterDTO(BaseModel):
    """用户注册DTO"""

    nickname: str = Field(description="用户昵称")
    password: str = Field(description="用户密码")


class UserLoginDTO(BaseModel):
    """用户登录DTO"""

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    account_id: str = Field(description="用户名")
    password: str = Field(description="用户密码")

class AdminLoginDTO(BaseModel):
    """管理员登录DTO"""
    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    admin_id: str = Field(description="管理员ID")
    password: str = Field(description="管理员密码")

class DeleteAccountDTO(BaseModel):
    """注销用户DTO"""
    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)
    account_id: str = Field(description="待注销的用户账号")


class GetSuggestionDTO(BaseModel):
    """查找用户建议DTO"""
    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)
    account_id: str = Field(description="待查找建议的用户账号")


class ChatMessageDTO(BaseModel):
    """用户发送的消息DTO"""

    message: str = Field(description="用户发送的消息内容")


class SuggestionDTO(BaseModel):
    """用户反馈信息DTO"""

    message: str = Field(default="", description="用户反馈的信息")
