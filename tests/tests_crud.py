# 与数据库进行交互
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from tests.tests_models import Books
from tests.tests_schemas import BooksBase

# 根据书籍 ID 获取书籍信息
async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(
        select(Books).where(Books.id == book_id)
    )
    return result.scalars().first()

# 根据书籍 名称 获取书籍信息
async def get_book_by_name(db:AsyncSession, book_name: str):
    result = await db.execute(
        select(Books).where(Books.name == book_name)
    )
    return result.scalars().first()

# 获取所有书籍信息，支持分页
async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Books).offset(skip).limit(limit)
    )
    return result.scalars().all()

# 查询书籍
async def search_book(db:AsyncSession):
    # 价格大于200
    '''result = await db.execute(
        select(tests_models.Books).where(tests_models.Books.price > 200)
    )'''
    # 模糊查询
    '''result = await db.execute(
       # select(tests_models.Books).where(tests_models.Books.name.like('我%') )
       # select(Books).where((Books.name.like('我%')) & (Books.price > 200))
    )'''
    # 根据list值查询
    id_list = [1,3,7]
    result = await db.execute(
        select(Books).where(Books.id.in_(id_list))
    )
    return result.scalars().all()

# 创建新书籍
async def create_book(db: AsyncSession, book: BooksBase):
    db_book = Books(
        name=book.name,
        author=book.author,
        isbn=book.isbn,
        price=book.price
    )
    db.add(db_book)
    await db.commit()  # 提交事务
    await db.refresh(db_book)  # 刷新对象，获取数据库生成的 id
    return db_book
