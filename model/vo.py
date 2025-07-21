from datetime import date as Date
from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class UserRegisterVO(BaseModel):
    """用户注册VO"""

    # 发送时转为 camelCase
    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    account_id: str = Field(description="用户账号ID")


class UserLoginVO(BaseModel):
    """用户登录VO"""

    token: str = Field(description="用户令牌")
    nickname: str = Field(description="用户昵称")


class CreateSessionVO(BaseModel):
    """创建会话VO"""

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    session_id: str = Field(description="会话ID")


class HistoryListVO(BaseModel):
    """历史会话列表VO"""

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    title: str = Field(description="会话标题")
    session_id: str = Field(description="会话id")


class HistoryTitleVO(BaseModel):
    """会话标题VO"""

    title: str = Field(description="会话标题")


class HistoryMessageVO(BaseModel):
    """历史消息VO"""

    role: str = Field(description="消息角色", examples=["human", "ai"])
    type: str = Field(description="消息类型", examples=["chat", "image", "plan", "audio"])
    message: str | dict = Field(description="消息内容")


class HotspotVO(BaseModel):
    """热门景点VO"""

    name: str = Field(description="景点名称")
    description: str = Field(description="景点描述")
    image: str = Field(description="景点图片URL")


class Weather(BaseModel):
    """一天天气"""

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    date: Date = Field(description="日期")
    max_degree: str = Field(description="最高温度")
    min_degree: str = Field(description="最低温度")
    day_weather: str = Field(description="白天天气")


class WeatherVO(BaseModel):
    """天气VO"""

    province: str = Field(description="省份")
    city: str = Field(description="城市")
    weathers: list[Weather] = Field(description="天气信息列表")
