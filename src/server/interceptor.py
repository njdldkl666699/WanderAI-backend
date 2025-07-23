import re
from typing import List

from fastapi import FastAPI, Request

from common.constant import JwtConstant, MessageConstant
from common.context import BaseContext
from common.database import get_db
from common.exception import UnauthorizedException
from common.log import log
from common.properties import JWT_TOKEN_NAME, RESOURCE_PATHS
from common.util import JwtUtil
from server.handler import handle_exception


def setup_middlewares(app: FastAPI):
    """按顺序设置所有中间件"""
    # 注意：这里的顺序是反向的，因为后注册先执行
    log.info("正在设置中间件...")
    setup_database_middleware(app)
    setup_user_jwt_middleware(app)
    setup_admin_jwt_middleware(app)


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


def setup_user_jwt_middleware(app: FastAPI):
    """校验用户jwt"""
    # 设置路径拦截器
    path_interceptor = PathMatcher()
    path_interceptor.add_path_patterns("/api/user/**")
    path_interceptor.exclude_path_patterns(["/api/user/user/login", "/api/user/user/register"])

    @app.middleware("http")
    async def user_jwt_middleware(request: Request, call_next):
        """校验用户jwt"""
        # 如果是OPTIONS请求（预检请求），直接放行
        if request.method == "OPTIONS":
            return await call_next(request)

        # 如果接口在白名单中，则不校验jwt
        if not path_interceptor.should_intercept(request.url.path):
            log.debug(f"请求路径 {request.url.path} 在白名单中，跳过JWT校验")
            return await call_next(request)

        try:
            log.debug(f"请求头： {request.headers}")
            token = request.headers.get(JWT_TOKEN_NAME, "")
            log.debug(f"请求头中的令牌: {token}")

            # 解析JWT令牌，如果解析失败会抛出异常
            payload = JwtUtil.parse_JWT(token)
            id: str | None = payload.get(JwtConstant.ACCOUNT_ID)
            if not id:
                raise UnauthorizedException(MessageConstant.JWT_INVALID_OR_EXPIRED)

            BaseContext.set_account_id(id)
            response = await call_next(request)
            return response
        except Exception as e:
            log.warning(f"JWT校验失败: {e}")
            return await handle_exception(
                request, UnauthorizedException(MessageConstant.JWT_INVALID_OR_EXPIRED)
            )


def setup_admin_jwt_middleware(app: FastAPI):
    """校验管理员jwt"""
    # 设置路径拦截器
    path_interceptor = PathMatcher()
    path_interceptor.add_path_patterns("/api/admin/**")
    path_interceptor.exclude_path_patterns("/api/admin/login")

    @app.middleware("http")
    async def admin_jwt_middleware(request: Request, call_next):
        """校验管理员jwt"""
        # 如果是OPTIONS请求（预检请求），直接放行
        if request.method == "OPTIONS":
            return await call_next(request)

        # 如果接口在白名单中，则不校验jwt
        if not path_interceptor.should_intercept(request.url.path):
            log.debug(f"请求路径 {request.url.path} 在白名单中，跳过JWT校验")
            return await call_next(request)

        try:
            log.debug(f"请求头： {request.headers}")
            token = request.headers.get(JWT_TOKEN_NAME, "")
            log.debug(f"请求头中的令牌: {token}")

            # 解析JWT令牌，如果解析失败会抛出异常
            payload = JwtUtil.parse_JWT(token)
            id: str | None = payload.get(JwtConstant.ADMIN_ID)
            if not id:
                raise UnauthorizedException(MessageConstant.JWT_INVALID_OR_EXPIRED)

            BaseContext.set_admin_id(id)
            response = await call_next(request)
            return response
        except Exception as e:
            log.warning(f"JWT校验失败: {e}")
            return await handle_exception(
                request, UnauthorizedException(MessageConstant.JWT_INVALID_OR_EXPIRED)
            )


class PathMatcher:
    """路径匹配器，用于拦截特定路径的请求"""

    def __init__(self):
        self.include_patterns: List[re.Pattern] = []
        self.exclude_patterns: List[re.Pattern] = self._compile_patterns(RESOURCE_PATHS)

    def add_path_patterns(self, patterns: str | List[str]) -> None:
        """添加拦截路径模式（支持 * 和 **）"""
        if isinstance(patterns, str):
            patterns = [patterns]
        self.include_patterns.extend(self._compile_patterns(patterns))

    def exclude_path_patterns(self, patterns: str | List[str]) -> None:
        """添加排除路径（支持精确匹配或模式匹配）"""
        if isinstance(patterns, str):
            patterns = [patterns]
        self.exclude_patterns.extend(self._compile_patterns(patterns))

    def should_intercept(self, path: str) -> bool:
        """检查路径是否需要拦截"""

        # 先检查是否在 exclude 列表
        for exclude_regex in self.exclude_patterns:
            if exclude_regex.fullmatch(path):
                return False

        # 再检查是否在 include 列表
        for include_regex in self.include_patterns:
            if include_regex.fullmatch(path):
                return True

        return False

    @staticmethod
    def _compile_patterns(patterns: List[str]) -> List[re.Pattern]:
        """将路径模式编译成正则表达式"""
        compiled = []
        for pattern in patterns:
            # 转义特殊字符，替换 * 和 **
            escaped = re.escape(pattern)
            regex = escaped.replace(r"\*\*", ".*").replace(r"\*", "[^/]+")
            compiled.append(re.compile(f"^{regex}$"))
        return compiled
