import logging
import re
import sys
from logging.handlers import TimedRotatingFileHandler

from common.properties import *


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
        # 添加颜色
        log_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"

        # 使用父类格式化
        return super().format(record)


def setup_logging():
    """统一配置所有日志"""
    # 配置根日志记录器
    root_logger = logging.getLogger()
    if DEBUG:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    # 清除现有处理器
    root_logger.handlers.clear()
    take_over_logging()

    # 创建控制台和文件处理器
    console_handler = create_console_handler()
    file_handler = create_file_handler()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    return root_logger


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
    if DEBUG:
        sqlalchemy_logger.setLevel(logging.INFO)  # 显示SQL语句
    else:
        sqlalchemy_logger.setLevel(logging.WARNING)

    # 清除 SQLAlchemy 的默认处理器
    sqlalchemy_logger.propagate = True

    # 配置其他常用库的日志
    logging.getLogger("fastapi").propagate = True
    logging.getLogger("asyncio").setLevel(logging.WARNING)


def create_console_handler():
    """创建控制台处理器"""
    # 创建控制台格式器
    console_formatter = ColoredFormatter(
        FORMAT,
        datefmt=DATEFMT,
    )
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    return console_handler


def create_file_handler():
    """创建文件处理器"""
    # 创建文件格式器
    file_formatter = logging.Formatter(
        FORMAT,
        datefmt=DATEFMT,
    )
    # 创建文件处理器
    file_handler = TimedRotatingFileHandler(
        filename=FILE_PREFIX, when=ROLL_WHEN, interval=INTERVAL  # 每天午夜切割日志
    )
    file_handler.setFormatter(file_formatter)
    # 设置日志文件后缀
    file_handler.suffix = FILE_SUFFIX
    # 匹配日期格式的日志文件
    file_handler.extMatch = re.compile(SUFFIX_REGEX)

    return file_handler


# 初始化日志配置
log = setup_logging()
