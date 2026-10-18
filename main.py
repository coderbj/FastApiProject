# 应用入口
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database import engine, Base
from users.users_router import router as users_router
from files.files_router import router as files_router
from tests.tests_router import router as tests_router

# 创建数据库表
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 在应用启动时初始化数据库
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # 初始化数据库，例如建表等
    yield  # 应用在此处开始接收请求

app = FastAPI(
    title="FastAPI Project",
    description="基于 FastAPI 和 SQLAlchemy 的用户管理系统",
    version="1.0.0",
    lifespan=lifespan
)



# 挂载静态文件目录
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


# 注册路由模块
app.include_router(users_router)
app.include_router(files_router)
app.include_router(tests_router)


@app.get("/")
def root():
    return {
        "message": "FastAPI 服务运行正常",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
