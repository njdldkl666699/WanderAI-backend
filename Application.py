import uvicorn

from common.log import setup_logging

if __name__ == "__main__":
    # 在启动服务器前配置日志
    logger = setup_logging()
    logger.info("正在启动 FastAPI 服务器...")

    # 启动服务器，禁用 uvicorn 的默认日志配置
    uvicorn.run(
        "server.app:app",
        port=8080,
        reload=True,
        log_config=None,  # 禁用 uvicorn 默认日志配置
        access_log=True,  # 启用访问日志
    )
