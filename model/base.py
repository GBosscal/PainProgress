import uuid
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, Boolean, func, VARCHAR
from datetime import datetime

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True  # 声明这是一个抽象基类，不会创建对应的数据库表格

    id = Column(VARCHAR(36), primary_key=True, default=str(uuid.uuid4()))
    created_time = Column(DateTime, default=datetime.now)
    updated_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_deleted = Column(Boolean, default=False)
