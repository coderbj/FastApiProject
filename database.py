# 数据库连接与 Session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase

# SQLite数据库
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"


# 创建数据库引擎
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread':False},
    pool_size=10,
    max_overflow=20
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# 声明基类
class Base(DeclarativeBase):
    pass


# 依赖项：获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
