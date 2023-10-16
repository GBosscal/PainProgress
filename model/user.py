"""
@Project: BackendForPain
@File: user.py
@Auth: Bosscal
@Date: 2023/9/4
@Description:
    用户表的具体描述。
"""
import traceback

from sqlalchemy import String, Column, Integer, DateTime, Boolean, Enum, VARCHAR

from model.base import BaseModel
from const import UserType, DeleteOrNot
from utils.orm_mysql import create_db_session

session = create_db_session()


class User(BaseModel):
    __tablename__ = "user"

    user_name = Column(VARCHAR(32), nullable=False)  # 用户名称
    hospital_id = Column(VARCHAR(36), nullable=False)  # 医院ID
    doctor_id = Column(VARCHAR(36), nullable=True)  # 医生ID
    user_type = Column(Enum(UserType), nullable=False)  # 用户类型
    age = Column(Integer, nullable=True)  # 年龄
    unionid = Column(VARCHAR(64), nullable=False)  # 微信ID（注册后应该能获取）

    def __init__(self, user_name, hospital_id, user_type, unionid, doctor_id=None, age=None, **kwargs):
        self.user_name = user_name
        self.hospital_id = hospital_id
        self.user_type = user_type
        self.unionid = unionid
        self.doctor_id = doctor_id
        self.age = age

    def to_dict(self):
        return {
            "user_name": self.user_name, "hospital_id": self.hospital_id, "age": self.age,
            "user_type": UserType(self.user_type).value, "doctor_id": self.doctor_id, "id": self.id,
        }

    @staticmethod
    def user_info_checker(user_info, ):
        """
        校验用户数据是否符合规定：
        1. 用户名称，医院ID，用户类型，wechatID不能为空。
        2. 用户类型为患者时，医生的ID不能为空。
        :param user_info:
        :return: bool
        """
        if not all([
            user_info.get("user_name"),
            user_info.get("hospital_id"),
            user_info.get("user_type"),
        ]):
            return False
        if not user_info.get("unionid") and not user_info.get("id"):
            return False
        # 转换用户的类型为标准类型
        try:
            user_info["user_type"] = UserType(user_info["user_type"]).value
        except KeyError:
            print(traceback.format_exc())
            return False
        # 校验患者类型的是否绑定了医生信息
        if user_info.get("user_type") == UserType.PATIENT.value and not user_info.get("doctor_id"):
            print("2")
            return False
        return True

    @classmethod
    def query_user_by_unionid(cls, unionid):
        """
        通过unionid查询用户
        :param unionid:
        :return:
        """
        return session.query(cls).filter_by(unionid=unionid, is_deleted=DeleteOrNot.NotDeleted.value).first()

    @classmethod
    def query_user_by_id(cls, user_id):
        """
        通过ID查询用户
        :param user_id:
        :return:
        """
        return session.query(cls).filter_by(id=user_id, is_deleted=DeleteOrNot.NotDeleted.value).first()

    @classmethod
    def add_user(cls, user_info):
        """
        新增用户
        :param user_info:
        :return:
        """
        try:
            new_user = cls(**user_info)
            session.add(new_user)
            session.commit()
            return True, new_user.id
        except Exception:
            print(traceback.format_exc())
            session.rollback()
            return False, None

    @classmethod
    def update_user(cls, user_info, user_data=None):
        if user_data is None:
            user_data = session.query(cls).filter_by(id=user_info["id"],
                                                     is_deleted=DeleteOrNot.NotDeleted.value).first()
        if not user_data:
            return False
        user_data.user_name = user_info["user_name"]
        user_data.user_type = user_info["user_type"]
        user_data.doctor_id = user_info["doctor_id"]
        user_data.hospital_id = user_info["hospital_id"]
        user_data.age = user_info["age"]
        try:
            session.merge(user_data)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False

    @classmethod
    def delete_user(cls, user_id, user_data=None):
        if user_data is None:
            user_data = session.query(cls).filte_by(id=user_id, is_deleted=DeleteOrNot.NotDeleted.value).first()
        if not user_data:
            return False
        user_data.is_deleted = DeleteOrNot.Deleted.value
        try:
            session.merge(user_data)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False

    @classmethod
    def query_user_by_doctor_id(cls, doctor_id):
        """
        通过医生的ID查询用户的信息
        :param doctor_id: 医生的ID
        :return:
        """
        return session.query(cls).filter_by(doctor_id=doctor_id, is_deleted=DeleteOrNot.NotDeleted.value).all()

    @classmethod
    def query_user_by_hospital_id(cls, hospital_id, user_type=None):
        """
        通过医院的ID查询用户信息
        """
        if not user_type:
            return session.query(cls).filter_by(hospital_id=hospital_id, is_deleted=DeleteOrNot.NotDeleted.value).all()
        else:
            return session.query(cls).filter_by(
                hospital_id=hospital_id, user_type=user_type, is_deleted=DeleteOrNot.NotDeleted.value
            ).all()
