from datetime import datetime, timedelta
from typing import Any

import alibabacloud_oss_v2 as oss
from jose import jwt

from common.constant import JwtConstant
from common.log import log
from common.properties import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    JWT_TTL_MINUTES,
    OSS_BUCKET_NAME,
    OSS_ENDPOINT,
    OSS_REGION,
)


class JwtUtil:
    """Jwt工具类"""

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


class AliOssUtil:
    """阿里OSS工具类"""

    # 从环境变量中加载凭证信息，用于身份验证
    credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()

    # 加载SDK的默认配置，并设置凭证提供者
    cfg = oss.config.load_default()
    cfg.credentials_provider = credentials_provider

    # 设置Region
    cfg.region = OSS_REGION

    # 使用配置好的信息创建OSS客户端
    client = oss.Client(cfg)

    @staticmethod
    def put_object(key: str, data: bytes) -> str:
        """向OSS存入数据

        Args:
            key (str): 数据的键（作为名称）
            data (bytes): 数据

        Returns:
            str: 数据对象的URL
        """
        try:
            AliOssUtil.client.put_object(
                oss.PutObjectRequest(bucket=OSS_BUCKET_NAME, key=key, body=data)
            )
            return f"https://{OSS_BUCKET_NAME}.{OSS_ENDPOINT}/{key}"
        except Exception as e:
            log.error("数据上传到阿里OSS失败", e)
            return ""
