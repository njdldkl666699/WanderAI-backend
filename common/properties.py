import os
from typing import Set

from dotenv import load_dotenv

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
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 地图API配置
AMAP_API_KEY = os.getenv("AMAP_API_KEY")
AMAP_MCP_URL = f"https://mcp.amap.com/mcp?key={AMAP_API_KEY}"

# Agent迭代次数配置
PLAN_AGENT_MAX_ITERATIONS = 4
EXECUTOR_AGENT_MAX_ITERATIONS = 1000
SUMMARY_AGENT_MAX_ITERATIONS = 4

# LLM配置
HOTSPOT_LLM_NAME = "qwen-plus"
INTENT_LLM_NAME = "qwen-turbo"
CHAT_LLM_NAME = "qwen-turbo"
PLAN_LLM_NAME = "qwen-turbo"
EXECUTOR_LLM_NAME = "qwen-max"
SUMMARY_LLM_NAME = "qwen-turbo"

# 温度配置
HOTSPOT_TEMPERATURE = 0.3
INTENT_TEMPERATURE = 0.2
CHAT_TEMPERATURE = 0.7
PLAN_TEMPERATURE = 0.2
EXECUTOR_TEMPERATURE = 0.2
SUMMARY_TEMPERATURE = 0.2
