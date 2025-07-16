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


class UserUpdateDTO(BaseModel):
    """用户修改昵称DTO"""

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    new_nickname: str = Field(description="用户新昵称")


class ChatMessageDTO(BaseModel):
    """用户发送的最新消息"""

    message: str = Field(description="用户发送的消息内容")
