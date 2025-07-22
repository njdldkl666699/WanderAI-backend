from pydantic import BaseModel, Field


class User(BaseModel):
    """用户模型"""

    account_id: str = Field(description="用户账号ID")
    nickname: str = Field(description="用户昵称")
    password: str = Field(description="用户密码")

    class Config:
        from_attributes = True  # 允许从ORM对象创建

class Admin(BaseModel):
    """管理员模型"""

    admin_id: str = Field(description="管理员ID")
    password: str = Field(description="管理员密码")

    class Config:
        from_attributes = True  # 允许从ORM对象创建

class UserHistory(BaseModel):
    """用户历史会话模型"""

    id: int | None = Field(default=None, description="主键")
    account_id: str = Field(description="用户账号ID")
    session_id: str = Field(description="会话ID")
    title: str = Field(description="历史会话标题")

    class Config:
        from_attributes = True


class Suggestion(BaseModel):
    """用户建议模型"""

    id: int |None = Field(None,description="建议ID")
    account_id: str = Field(description="用户账号ID")
    message: str = Field(description="建议内容")

    class Config:
        from_attributes = True
