import uvicorn

from wanderai.common.log import log
from wanderai.common.properties import (
    UVICORN_HOST,
    UVICORN_PORT,
    UVICORN_TIMEOUT_KEEP_ALIVE,
)
from wanderai.server.app import app


def main():
    # 在启动服务器前配置日志
    log.info("正在启动 FastAPI 服务器...")

    # 启动服务器，禁用 uvicorn 的默认日志配置
    uvicorn.run(
        app,
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        reload=False,  # 调试时禁用热重载
        log_config=None,  # 禁用 uvicorn 默认日志配置
        access_log=True,  # 启用访问日志
        timeout_keep_alive=UVICORN_TIMEOUT_KEEP_ALIVE,
    )


if __name__ == "__main__":
    main()
