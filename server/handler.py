from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from common.exception import AppException, UnauthorizedException
from common.log import log
from model.result import Result


def get_status_code(exc: Exception) -> tuple[int, str]:
    """获取异常的状态码"""
    if isinstance(exc, UnauthorizedException):
        return status.HTTP_401_UNAUTHORIZED, "未授权访问"

    if isinstance(exc, AppException):
        return status.HTTP_400_BAD_REQUEST, str(exc)

    # 其他异常返回500，可根据需要添加更多异常类型
    return status.HTTP_500_INTERNAL_SERVER_ERROR, "服务器内部错误"


# 全局异常处理器
async def handle_exception(request, exc: Exception):
    """全局异常处理器"""
    log.error(f"发生异常: {exc}")
    status_code, message = get_status_code(exc)
    if status_code >= 500:
        log.error(f"服务器错误 [{status_code}]：{exc}", exc_info=True)
    else:
        log.warning(f"客户端错误 [{status_code}]：{message}")
    result = Result.error(message)
    return JSONResponse(status_code=status_code, content=result.model_dump())


# 设置全局异常处理器
def setup_exception_handler(app: FastAPI):
    """设置异常处理器"""
    log.info("正在设置全局异常处理器...")
    app.add_exception_handler(Exception, handle_exception)
