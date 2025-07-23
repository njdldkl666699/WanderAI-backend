from pydantic import BaseModel, ConfigDict, Field
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


class DeleteSuggestionDTO(BaseModel):
    """删除用户建议DTO"""

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)
    id: int = Field(description="待删除的用户建议ID")


class ChatMessageDTO(BaseModel):
    """用户发送的消息DTO"""

    message: str = Field(description="用户发送的消息内容")


class SuggestionDTO(BaseModel):
    """用户反馈信息DTO"""

    message: str = Field(default="", description="用户反馈的信息")


class GuideMessageDTO(BaseModel):
    """导游消息DTO"""

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    image_url: str = Field(description="导游发送的图片URL")
    message: str = Field(description="导游发送的消息内容")
