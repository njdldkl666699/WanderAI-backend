from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class UserLoginVO(BaseModel):
    id: int
    name: str
    password: str | None = None
    create_time: datetime | None = None
    token: str | None = None


class CreateSessionVO(BaseModel):
    """创建会话VO"""

    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)

    session_id: str = Field(description="会话ID")
