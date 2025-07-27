from contextlib import asynccontextmanager
from typing import AsyncGenerator

from redis import StrictRedis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from wanderai.common.log import log
from wanderai.common.properties import (
    DATABASE_URL,
    DB_MAX_OVERFLOW,
    DB_POOL_SIZE,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PASSWORD,
    REDIS_PORT,
)
from wanderai.model.schema import Base

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


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话的依赖项"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            log.info("提交数据库事务...")
            await session.commit()
        except Exception:
            log.warning("回滚数据库事务...")
            await session.rollback()
            raise
        finally:
            await session.close()


redis = StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True
)
