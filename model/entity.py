from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, SecretStr


class Student(BaseModel):
    ID: str
    name: str
    dept_name: str | None = None
    tot_cred: Decimal | None = None

    class Config:
        from_attributes = True  # 允许从ORM对象创建


class User(BaseModel):
    id: int
    name: str
    password: str | None = None
    create_time: datetime | None = None

    class Config:
        from_attributes = True  # 允许从ORM对象创建


class ChatModelEntity(BaseModel):
    model: str
    temperature: float = 0.7
    base_url: str
    api_key: SecretStr
    max_tokens: int | None = None
