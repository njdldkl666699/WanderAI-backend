import atexit
import copy
import logging
import os
import sys
from datetime import datetime

from wanderai.common.properties import LOG_DATEFMT, LOG_FILE_PREFIX, LOG_FORMAT, LOG_LEVEL


# 日志配置
class ColoredFormatter(logging.Formatter):
    """自定义彩色格式器"""

    # ANSI 颜色代码
    COLORS = {
        "DEBUG": "\033[36m",  # 青色
        "INFO": "\033[32m",  # 绿色
        "WARNING": "\033[33m",  # 黄色
        "ERROR": "\033[31m",  # 红色
        "CRITICAL": "\033[41m",  # 红色背景
        "RESET": "\033[0m",  # 重置
    }

    def format(self, record):
        # 创建 record 的副本，避免修改原始 record

        record_copy = copy.copy(record)

        # 为副本添加颜色
        log_color = self.COLORS.get(record_copy.levelname, self.COLORS["RESET"])
        record_copy.levelname = f"{log_color}{record_copy.levelname}{self.COLORS['RESET']}"

        # 使用父类格式化副本
        return super().format(record_copy)


def setup_logging():
    """统一配置所有日志"""
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)

    # 清除现有处理器
    root_logger.handlers.clear()
    take_over_logging()

    # 创建控制台和文件处理器
    console_handler = create_console_handler()
    file_handler = create_file_handler()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # 配置在程序关闭时禁用日志记录
    atexit.register(disable_logging_on_shutdown)

    return root_logger


def disable_logging_on_shutdown():
    """程序关闭时禁用日志记录"""
    logging.disable(logging.CRITICAL)
    # 同时禁用所有第三方库的日志
    for name in ["httpcore", "httpx", "openai"]:
        logger = logging.getLogger(name)
        logger.disabled = True


def take_over_logging():
    """重新配置日志，使用新的日志配置"""
    # 配置 uvicorn 日志
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_error_logger = logging.getLogger("uvicorn.error")
    uvicorn_logger = logging.getLogger("uvicorn")

    # 设置 uvicorn 日志级别
    uvicorn_logger.setLevel(logging.INFO)
    uvicorn_access_logger.setLevel(logging.INFO)
    uvicorn_error_logger.setLevel(logging.INFO)

    # 禁用 uvicorn 的默认处理器，使用我们的处理器
    uvicorn_logger.propagate = True
    uvicorn_access_logger.propagate = True
    uvicorn_error_logger.propagate = True

    # 配置 SQLAlchemy 日志
    sqlalchemy_logger = logging.getLogger("sqlalchemy")
    if LOG_LEVEL == "DEBUG":
        sqlalchemy_logger.setLevel(logging.INFO)  # 显示SQL语句
    else:
        sqlalchemy_logger.setLevel(logging.WARNING)

    # 清除 SQLAlchemy 的默认处理器
    sqlalchemy_logger.propagate = True

    # 配置特定库的日志级别为 INFO，除非设定为最低等级
    if LOG_LEVEL != "NOTSET":
        logging.getLogger("openai._base_client").setLevel(logging.INFO)
        logging.getLogger("httpcore.http11").setLevel(logging.INFO)
        logging.getLogger("urllib3.connectionpool").setLevel(logging.INFO)
        logging.getLogger("httpcore.connection").setLevel(logging.INFO)
        logging.getLogger("mcp.client.streamable_http").setLevel(logging.INFO)
        logging.getLogger("langsmith.client").setLevel(logging.INFO)
        logging.getLogger("dashscope").setLevel(logging.INFO)


def create_console_handler():
    """创建控制台处理器"""
    # 创建控制台格式器
    console_formatter = ColoredFormatter(
        LOG_FORMAT,
        datefmt=LOG_DATEFMT,
    )
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    return console_handler


def create_file_handler():
    """创建文件处理器"""

    # 确保日志目录存在
    log_dir = os.path.dirname(LOG_FILE_PREFIX)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建文件格式器
    file_formatter = logging.Formatter(
        LOG_FORMAT,
        datefmt=LOG_DATEFMT,
    )

    # 生成带日期的文件名
    current_date = datetime.now().strftime("%Y-%m-%d")
    daily_filename = f"{LOG_FILE_PREFIX}.{current_date}.log"

    # 使用普通的 FileHandler，每天程序启动时自动创建新文件
    file_handler = logging.FileHandler(filename=daily_filename, mode="a", encoding="utf-8")
    file_handler.setFormatter(file_formatter)

    return file_handler


# 初始化日志配置
log = setup_logging()
