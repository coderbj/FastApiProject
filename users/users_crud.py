# 与数据库进行交互
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from users.users_models import User
from users.users_schemas import UserCreate


# 根据 ID 获取用户
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


# 根据邮箱获取用户
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


# 获取用户列表
async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


# 创建用户
async def create_user(db: AsyncSession, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"  # 实际应使用 passlib 哈希
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalars().first()
    if not db_user:
        db_user = User(
            email=user.email,
            hashed_password=fake_hashed_password
        )
        db.add(db_user)
    await db.commit()  # 提交事务
    await db.refresh(db_user)  # 刷新对象，获取数据库生成的 id
    return db_user
