# SQLAlchemy ORM 模型，告诉 SQLAlchemy：这个类对应哪张表、每个属性对应哪一列。
from sqlalchemy import Column, Integer, String, Boolean, Numeric
from database import Base


class Books(Base):
    __tablename__ = "books"  # 表名

    id = Column(Integer, primary_key=True, index=True)  # 主键，自增
    name = Column(String, unique=True, index=True)      # 唯一，建索引
    author = Column(String, nullable=False)             # 作者
    isbn = Column(String, unique=True, index=True)      # ISBN
    price = Column(Numeric(10, 2), nullable=False)              # 价格

