from datetime import datetime, timedelta
from typing import Any

from jose import jwt

from common.constant.JwtConstant import EXPIRATION
from common.properties import ALGORITHM, SECRET_KEY, TTL_MINUTES


class JwtUtil:

    @staticmethod
    def create_JWT(data: dict[str, Any]):
        """创建访问令牌"""
        to_encode = data.copy()

        expire = datetime.now() + timedelta(minutes=TTL_MINUTES)

        to_encode.update({EXPIRATION: expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    @staticmethod
    def parse_JWT(token: str) -> dict[str, Any] | None:
        """解析访问令牌"""
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        exp = payload.get(EXPIRATION)
        if exp is None:
            # 如果没有过期时间，令牌无效
            return None
        if datetime.fromtimestamp(exp) < datetime.now():
            # 如果当前时间超过过期时间，令牌无效
            return None

        return payload
