"""
@Project: BackendForPain
@File: orm_mysql.py
@Auth: Bosscal
@Date: 2023/9/4
@Description:
    通过ORM的形式，操作mysql数据库。
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import Config


def create_db_session():
    engine = create_engine(Config.get_mysql_url(), echo=Config.MysqlEcho, pool_pre_ping=True)
    session = sessionmaker(bind=engine)
    return session()

