"""
@Project: BackendForPain
@File: hospital.py
@Auth: Bosscal
@Date: 2023/9/12
@Description: 
"""
from model.hospital import Hospital
from const import ErrorCode


class HospitalService:

    @classmethod
    async def get_hospitals(cls):
        """
        获取医院的列表
        :return:
        """
        return [data.to_dict() for data in Hospital.get_hospitals() or []]

    @classmethod
    async def add_hospital(cls, name):
        """
        新增一个医院
        :param name:
        :return:
        """
        # 检查医院名称是否重复
        if Hospital.query_hospital_by_name(name):
            return ErrorCode.HospitalExists
        # 新增医院
        if Hospital.add_hospital(name):
            return ErrorCode.Success
        return ErrorCode.HospitalAddError

    @classmethod
    async def update_hospital(cls, hospital_id, name):
        """
        更新医院的名称
        :param hospital_id:
        :param name:
        :return:
        """
        # 检查医院是否存在
        hospital_data = Hospital.query_hospital_by_id(hospital_id)
        if not hospital_data:
            return ErrorCode.HospitalNotExists
        # 更新医院的信息
        if not Hospital.update_hospital(name, hospital_data):
            return ErrorCode.HospitalUpdateError
        return ErrorCode.Success

    @classmethod
    async def delete_hospital(cls, hospital_id):
        """
        删除医院
        :param hospital_id:
        :return:
        """
        # 检查医院是否存在
        hospital_data = Hospital.query_hospital_by_id(hospital_id)
        if not hospital_data:
            return ErrorCode.HospitalNotExists
        # 删除医院
        if not Hospital.delete_hospital(hospital_data):
            return ErrorCode.HospitalDeleteError
        return ErrorCode.Success
