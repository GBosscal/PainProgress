"""
@Project: BackendForPain
@File: user.py
@Auth: Bosscal
@Date: 2023/9/4
@Description:
    医院表的具体描述。
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR

from model.base import BaseModel
from utils.orm_mysql import create_db_session
from const import DeleteOrNot


class Hospital(BaseModel):
    __tablename__ = "hospital"

    name = Column(VARCHAR(64), nullable=True)  # 医院名称

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {"name": self.name, "id": self.id}

    @classmethod
    def get_hospitals(cls):
        with create_db_session() as session:
            return session.query(cls).filter_by(is_deleted=DeleteOrNot.NotDeleted.value).all()

    @classmethod
    def add_hospital(cls, name):
        new_hospital = cls(name=name)
        with create_db_session() as session:
            try:
                session.add(new_hospital)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False

    @classmethod
    def update_hospital(cls, name, data):
        data.name = name
        with create_db_session() as session:
            try:
                session.merge(data)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False

    @classmethod
    def delete_hospital(cls, data):
        data.is_deleted = DeleteOrNot.Deleted.value
        with create_db_session() as session:
            try:
                session.merge(data)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False

    @classmethod
    def query_hospital_by_id(cls, _id):
        with create_db_session() as session:
            return session.query(cls).filter_by(id=_id).first()

    @classmethod
    def query_hospital_by_name(cls, name):
        with create_db_session() as session:
            return session.query(cls).filter_by(name=name).all()
