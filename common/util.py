from datetime import datetime, timedelta
from typing import Any

from jose import jwt
from common.constant import JwtConstant

from common.properties import JWT_ALGORITHM, JWT_SECRET_KEY, JWT_TTL_MINUTES


class JwtUtil:

    @staticmethod
    def create_JWT(data: dict[str, Any]):
        """创建访问令牌"""
        to_encode = data.copy()

        expire = datetime.now() + timedelta(minutes=JWT_TTL_MINUTES)

        to_encode.update({JwtConstant.EXPIRATION: expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

        return encoded_jwt

    @staticmethod
    def parse_JWT(token: str) -> dict[str, Any] | None:
        """解析访问令牌"""
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

        exp = payload.get(JwtConstant.EXPIRATION)
        if exp is None:
            # 如果没有过期时间，令牌无效
            return None
        if datetime.fromtimestamp(exp) < datetime.now():
            # 如果当前时间超过过期时间，令牌无效
            return None

        return payload
