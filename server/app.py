from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from common.database import init_db
from server.controller import ChatController, StudentController, UserController
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
    allow_origins=["http://localhost:7070"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 设置全局异常处理器
setup_exception_handler(app)

# 设置中间件
setup_middlewares(app)

api_router = APIRouter(prefix="/api")
api_router.include_router(StudentController.router)
api_router.include_router(UserController.router)
api_router.include_router(ChatController.router)

app.include_router(api_router)
