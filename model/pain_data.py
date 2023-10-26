"""
@Project: BackendForPain
@File: user.py
@Auth: Bosscal
@Date: 2023/9/4
@Description:
    疼痛数据表的具体描述。
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR

from model.base import BaseModel
from utils.orm_mysql import create_db_session
from const import DeleteOrNot



class Pain(BaseModel):
    __tablename__ = "pain_data"

    patient_id = Column(VARCHAR(36), nullable=False)  # 患者ID
    pain_level_custom = Column(Integer, nullable=False)  # 患者输入的疼痛等级
    pain_level = Column(VARCHAR(32), nullable=True)  # 模型计算后得到的疼痛等级
    pain_data_path = Column(VARCHAR(128), nullable=False)  # 疼痛数据存储的位置

    def __init__(self, patient_id, pain_level_custom, pain_data, pain_level=None):
        self.patient_id = patient_id
        self.pain_level_custom = pain_level_custom
        self.pain_data_path = pain_data
        self.pain_level = pain_level

    def to_dict(self):
        return {
            "patient_id": self.patient_id, "pain_level_custom": self.pain_level_custom,
            "pain_level": self.pain_level, "pain_data": self.pain_data_path,
            "created_time": self.created_time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_time": self.updated_time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @classmethod
    def query_pain_data_by_id(cls, pain_id):
        with create_db_session() as session:
            return session.query(cls).filter_by(id=pain_id).first()

    @classmethod
    def query_pain_data_by_patient_id(cls, patient_id):
        with create_db_session() as session:
            return session.query(cls).filter_by(
                patient_id=patient_id, is_deleted=DeleteOrNot.NotDeleted.value
            ).order_by(cls.created_time).all()

    @classmethod
    def add_pain_data(cls, **kwargs):
        new_pain = cls(**kwargs)
        with create_db_session() as session:
            try:
                session.add(new_pain)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False

    @classmethod
    def update_pain_data(cls, pain_level_custom, pain_data_path, pain_data, pain_level=None):
        pain_data.pain_level_custom = pain_level_custom
        pain_data.pain_data_path = pain_data_path
        pain_data.pain_level = pain_level
        with create_db_session() as session:
            try:
                session.merge(pain_data)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False

    @classmethod
    def delete_pain_data(cls, pain_data):
        pain_data.is_deleted = DeleteOrNot.Deleted.value
        with create_db_session() as session:
            try:
                session.merge(pain_data)
                session.commit()
                return True
            except Exception:
                print(traceback.format_exc())
                session.rollback()
                return False
