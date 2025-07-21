from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.database import init_db
from server.controller import (
    ChatController,
    HistoryController,
    HotspotController,
    SuggestionController,
    UserController,
    AdminController,
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

api_router = APIRouter(prefix="/api")
api_router.include_router(UserController.router)
api_router.include_router(ChatController.router)
api_router.include_router(HotspotController.router)
api_router.include_router(HistoryController.router)
api_router.include_router(SuggestionController.router)
api_router.include_router(AdminController.router)

app.include_router(api_router)
