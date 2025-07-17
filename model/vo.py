from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class UserLoginVO(BaseModel):
    """用户登录VO"""

    token: str = Field(description="用户令牌")
    nickname: str = Field(description="用户昵称")


class UserRegisterVO(BaseModel):
    """用户注册VO"""

    # 发送时转为 camelCase
    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    account_id: str = Field(description="用户账号ID")


class CreateSessionVO(BaseModel):
    """创建会话VO"""

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    session_id: str = Field(description="会话ID")


class HistoryTitleVO(BaseModel):
    """历史会话标题VO"""

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    title: str = Field(description="会话标题")


class HistoryMessageVO(BaseModel):
    """历史消息VO"""

    type: str = Field(description="消息类型")
    message: str | list[dict]= Field(description="消息内容")


class HotspotVO(BaseModel):
    """热门景点VO"""

    name: str = Field(description="景点名称")
    description: str = Field(description="景点描述")
    image: str = Field(description="景点图片URL")
