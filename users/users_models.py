# SQLAlchemy ORM 模型，告诉 SQLAlchemy：这个类对应哪张表、每个属性对应哪一列。
from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class User(Base):
    __tablename__ = "users"  # 表名

    id = Column(Integer, primary_key=True, index=True)  # 主键，自增
    email = Column(String, unique=True, index=True)      # 唯一，建索引
    hashed_password = Column(String)                      # 哈希密码
    is_active = Column(Boolean, default=True)             # 是否活跃

