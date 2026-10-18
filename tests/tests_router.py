# APIRouter 路由模块
from fastapi import APIRouter, Depends, HTTPException
from tests import tests_schemas, tests_crud
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter(
    prefix='/test',  # 所有路由自动加上前缀
    tags=['测试'],  # Swagger 文档中的分组标签
)

# 查询书籍 价格 大于200的
@router.get('/books/search_book')
async def search_book(db:AsyncSession = Depends(get_db)):
    db_book = await tests_crud.search_book(db)
    return db_book

# 根据书籍 ID 获取书籍信息
@router.get('/books/{book_id}', response_model=tests_schemas.BooksBase)
async def read_book(book_id: int, db:AsyncSession = Depends(get_db)):
    db_book = await tests_crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="书籍不存在")
    return db_book

# 创建新书籍
@router.post('/books', response_model=tests_schemas.BooksBase)
async def create_book(book:tests_schemas.BooksBase, db:AsyncSession = Depends(get_db)):
    db_book = await tests_crud.get_book_by_name(db, book.name)
    if db_book is not None:
        raise HTTPException(status_code=409, detail='书籍已存在')
    return await tests_crud.create_book(db, book)