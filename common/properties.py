import os
from typing import Set

from dotenv import load_dotenv
from pydantic import SecretStr

from model.entity import ChatModelEntity

# 配置文件
load_dotenv()

# 数据库配置
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 异步数据库URL (使用asyncmy驱动)
DATABASE_URL = f"mysql+asyncmy://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))  # 数据库连接池大小
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))  # 数据库连接池最大溢出连接数

# 日志配置
DEBUG = os.getenv("DEBUG", "True").lower() == "true"  # 是否开启调试模式
FORMAT = os.getenv("FORMAT", "%(asctime)s [%(levelname)s] [%(name)s] - %(message)s")
DATEFMT = os.getenv("DATEFMT", "%Y-%m-%d %H:%M:%S")
FILE_PREFIX = os.getenv("FILE_PREFIX", "./logs/app")
ROLL_WHEN = os.getenv("ROLL_WHEN", "midnight")  # 日志切割时间
INTERVAL = int(os.getenv("INTERVAL", "1"))  # 切割间隔
FILE_SUFFIX = os.getenv("FILE_SUFFIX", "%Y-%m-%d.log")  # 日志文件后缀
SUFFIX_REGEX = os.getenv(
    "SUFFIX_REGEX", r"^\d{4}-\d{2}-\d{2}.log$"
)  # 日志文件名匹配正则

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "")
TTL_MINUTES = int(os.getenv("TTL_MINUTES", "300"))
ALGORITHM = os.getenv("ALGORITHM", "HS256")
TOKEN_NAME = os.getenv("TOKEN_NAME", "Authentication")  # JWT令牌名称

# JWT校验白名单
WHITELIST_PATHS: Set[str] = {
    "/api/user/login",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
    "/health",
}


# 大模型配置
QWEN_API_KEY = os.getenv("API_KEY", "")
QWEN_BASE_URL = os.getenv(
    "QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 聊天模型配置
DEFAULT_MODE = "qwen-turbo"
CHAT_MODELS = {
    "qwen-plus": ChatModelEntity(
        model="qwen-plus",
        temperature=0.7,
        base_url=QWEN_BASE_URL,
        api_key=SecretStr(QWEN_API_KEY),
    ),
    "qwen-turbo": ChatModelEntity(
        model="qwen-turbo",
        temperature=0.7,
        base_url=QWEN_BASE_URL,
        api_key=SecretStr(QWEN_API_KEY),
    ),
    "qwen-max": ChatModelEntity(
        model="qwen-max",
        temperature=0.7,
        base_url=QWEN_BASE_URL,
        api_key=SecretStr(QWEN_API_KEY),
    ),
    "deepseek-r1-0528": ChatModelEntity(
        model="deepseek-r1-0528",
        temperature=0.7,
        base_url=QWEN_BASE_URL,
        api_key=SecretStr(QWEN_API_KEY),
    ),
    "deepseek-v3": ChatModelEntity(
        model="deepseek-v3",
        temperature=0.7,
        base_url=QWEN_BASE_URL,
        api_key=SecretStr(QWEN_API_KEY),
    ),
}
