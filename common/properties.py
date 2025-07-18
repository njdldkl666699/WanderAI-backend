import os
from typing import Set

from dotenv import load_dotenv
from pydantic import BaseModel, Field, SecretStr

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


# Redis配置
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")  # 日志级别
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s [%(levelname)s] [%(name)s] - %(message)s")
LOG_DATEFMT = os.getenv("LOG_DATEFMT", "%Y-%m-%d %H:%M:%S")
LOG_FILE_PREFIX = os.getenv("LOG_FILE_PREFIX", "./logs/wanderai")  # 日志文件前缀
LOG_ROLL_WHEN = os.getenv("LOG_ROLL_WHEN", "midnight")  # 日志切割时间
LOG_INTERVAL = int(os.getenv("LOG_INTERVAL", "1"))  # 切割间隔
LOG_FILE_SUFFIX = os.getenv("LOG_FILE_SUFFIX", "%Y-%m-%d.log")  # 日志文件后缀
LOG_SUFFIX_REGEX = os.getenv("LOG_SUFFIX_REGEX", r"^\d{4}-\d{2}-\d{2}.log$")  # 日志文件名匹配正则


# JWT配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
JWT_TTL_MINUTES = int(os.getenv("JWT_TTL_MINUTES", "300"))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_TOKEN_NAME = os.getenv("JWT_TOKEN_NAME", "Authentication")  # JWT令牌名称

# JWT校验白名单
WHITELIST_PATHS: Set[str] = {
    "/api/user/login",
    "/api/user/register",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
    "/health",
}


# 大模型配置
QWEN_API_KEY = SecretStr(os.getenv("QWEN_API_KEY", ""))
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 地图API配置
AMAP_API_KEY = os.getenv("AMAP_API_KEY")
AMAP_MCP_URL = f"https://mcp.amap.com/mcp?key={AMAP_API_KEY}"

# Agent迭代次数配置
PLAN_AGENT_MAX_ITERATIONS = 4
EXECUTOR_AGENT_MAX_ITERATIONS = 1000
SUMMARY_AGENT_MAX_ITERATIONS = 4


class LLMConfig(BaseModel):
    """LLM配置类"""

    model: str = Field(description="LLM模型名称")
    api_key: SecretStr = Field(description="API密钥")
    base_url: str = Field(default="", description="API基础URL")
    temperature: float | None = Field(default=0.7, description="生成文本的温度参数")


# 热门景点LLM配置
HOTSPOT_CONFIG = LLMConfig(
    model="qwen-plus",
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL,
    temperature=0.3,
)

# 聊天标题LLM配置
TITLE_CONFIG = LLMConfig(
    model="qwen-turbo",
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL,
    temperature=0.7,
)

# 意图识别LLM配置
INTENT_CONFIG = LLMConfig(
    model="qwen-turbo",
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL,
    temperature=0.2,
)

# 聊天LLM配置
CHAT_CONFIG = LLMConfig(
    model="qwen-turbo",
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL,
    temperature=0.7,
)

# 旅行计划LLM配置
PLAN_CONFIG = LLMConfig(
    model="qwen-turbo",
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL,
    temperature=0.2,
)

# 每日规划LLM配置
EXECUTOR_CONFIG = LLMConfig(
    model="qwen-max",
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL,
    temperature=0.2,
)

# 总结LLM配置
SUMMARY_CONFIG = LLMConfig(
    model="qwen-turbo",
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL,
    temperature=0.2,
)

# 图像理解LLM配置
VISUAL_CONFIG = LLMConfig(
    model="qwen-vl-plus",
    api_key=QWEN_API_KEY,
    base_url=QWEN_BASE_URL,
    temperature=None,
)
