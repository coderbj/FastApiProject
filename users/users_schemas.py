# Pydantic Schema（FastAPI 独有）
from pydantic import ConfigDict
from pydantic import BaseModel

# 用户模型
class UserBase(BaseModel):
    email:str

class UserCreate(UserBase):
    password:str # 创建时需要密码

class UserOut(UserBase):
    id:int
    is_active:bool

    model_config = ConfigDict(from_attributes=True)

