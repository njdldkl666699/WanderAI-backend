from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.database import init_db
from server.controller import (
    AdminController,
    ChatController,
    HistoryController,
    HotspotController,
    SuggestionController,
    UploadController,
    UserController,
)
from server.handler import setup_exception_handler
from server.interceptor import setup_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


# app配置
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 设置全局异常处理器
setup_exception_handler(app)

# 设置中间件
setup_middlewares(app)

# 根路由
api_router = APIRouter(prefix="/api")

# 用户组路由，例如/api/user/user/login
user_router = APIRouter(prefix="/user")
user_router.include_router(UserController.router)
user_router.include_router(ChatController.router)
user_router.include_router(HotspotController.router)
user_router.include_router(HistoryController.router)
user_router.include_router(SuggestionController.router)
user_router.include_router(UploadController.router)
api_router.include_router(user_router)

# 管理路由，例如/api/admin/login
api_router.include_router(AdminController.router)

# 添加到APP
app.include_router(api_router)
