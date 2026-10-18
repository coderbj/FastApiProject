# APIRouter 路由模块
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from users import users_crud, users_schemas

router = APIRouter(
    prefix="/users", # 所有路由自动加上前缀
    tags=["用户"], # Swagger 文档中的分组标签
)


@router.post("", response_model=users_schemas.UserOut, status_code=status.HTTP_201_CREATED)

@router.post("/", response_model=users_schemas.UserOut, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_user(user: users_schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    # 检查邮箱是否已存在
    db_user = await users_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已注册")
    return await users_crud.create_user(db=db, user=user)

@router.get("", response_model=list[users_schemas.UserOut])

@router.get("/", response_model=list[users_schemas.UserOut], include_in_schema=False)
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    users = await users_crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=users_schemas.UserOut)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await users_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    return db_user

