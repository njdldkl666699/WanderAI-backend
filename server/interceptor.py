from fastapi import FastAPI, Request

from common.constant.JwtConstant import ACCOUNT_ID
from common.constant.MessageConstant import JWT_INVALID_OR_EXPIRED, PLEASE_LOGIN
from common.context import BaseContext
from common.database import get_db
from common.exception import UnauthorizedException
from common.log import log
from common.properties import TOKEN_NAME, WHITELIST_PATHS
from common.util import JwtUtil
from server.handler import handle_exception


def setup_middlewares(app: FastAPI):
    """按顺序设置所有中间件"""
    # 注意：这里的顺序是反向的，因为后注册先执行
    log.info("正在设置中间件...")
    setup_database_middleware(app)
    setup_jwt_middleware(app)


def setup_database_middleware(app: FastAPI):
    @app.middleware("http")
    async def db_middleware(request: Request, call_next):
        """数据库中间件"""
        try:
            async with get_db() as db:
                BaseContext.set_db_session(db)
                response = await call_next(request)
                return response
        except Exception as e:
            return await handle_exception(request, e)


def setup_jwt_middleware(app: FastAPI):
    @app.middleware("http")
    async def jwt_middleware(request: Request, call_next):
        """校验jwt"""
        try:
            # 如果是OPTIONS请求（预检请求），直接放行
            if request.method == "OPTIONS":
                return await call_next(request)

            # 如果是/user/login接口，则不校验jwt
            if request.url.path in WHITELIST_PATHS:
                return await call_next(request)

            log.debug(f"请求头： {request.headers}")
            token = request.headers.get(TOKEN_NAME)
            log.debug(f"请求头中的令牌: {token}")
            if not token:
                raise UnauthorizedException(PLEASE_LOGIN)

            payload = JwtUtil.parse_JWT(token)
            if not payload:
                raise UnauthorizedException(JWT_INVALID_OR_EXPIRED)

            id = payload.get(ACCOUNT_ID)
            if not id:
                raise UnauthorizedException(JWT_INVALID_OR_EXPIRED)

            BaseContext.set_account_id(id)
            response = await call_next(request)
            return response
        except Exception as e:
            return await handle_exception(request, e)
