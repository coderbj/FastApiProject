# Pydantic Schema（FastAPI 独有）
from pydantic import BaseModel

# 书籍模型
class BooksBase(BaseModel):
    name:str
    author:str
    isbn:str
    price:float

