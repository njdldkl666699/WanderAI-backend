from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from common.properties import *
from model.schema import Base
from common.log import log

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)

# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def init_db():
    """初始化数据库表"""
    async with engine.begin() as conn:
        log.info("正在初始化数据库...")
        await conn.run_sync(Base.metadata.create_all)
