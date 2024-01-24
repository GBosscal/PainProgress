from model.user import User
from model.hospital import Hospital
from const import ErrorCode, UserType, PreUserID
from utils.wechat_scripts import get_user_info_by_code
from config import Config
from utils.secret import hash_password

import random
from uuid import uuid4


class UserService:

    @classmethod
    async def _add_user(cls, user_info):
        """
        (内部方法)将用户新增到数据库中
        :param user_info:
        """
        # 查询名称为华侨医院的id
        hp_id, _ = Hospital.query_huaqiao_hospital()
        user_info["hospital_id"] = hp_id
        # 检验数据是否缺失
        if not User.user_info_checker(user_info):
            return ErrorCode.UserInfoError, None
        # 校验用户（同一个微信ID）是否存在
        if User.query_user_by_unionid(user_info["unionid"]) is not None:
            return ErrorCode.UserAlreadyExists, None
        # 校验用户是否重名，如果重名的话则在后面增加序号
        name_index = User.query_name_by_user_name(user_info["user_name"])
        if name_index is not None:
            user_info["user_name"] = f"{user_info['user_name']} - {str(name_index + 1)}"
        # 密码加密存储
        if user_info["password"]:
            user_info["password"] = hash_password(user_info["password"])
        # 新增用户
        status, user_id = User.add_user(user_info)
        if not status:
            return ErrorCode.UserAddError, None
        user_info.update({"id": user_id})
        if not user_info.get("service_unionid"):
            user_info.pop("unionid", None)
        return ErrorCode.Success, user_info

    @classmethod
    async def add_user_by_service_unionid(cls, user_info):
        """
        通过service_unionid去新增用户
        从PreUserID开始，每一个新增的用户增加1
        """
        max_id = User.query_max_service_unionid()
        service_unionid = max_id + 1
        unionid = service_unionid + PreUserID
        user_info["unionid"] = unionid
        user_info["service_unionid"] = service_unionid
        status, data = await cls._add_user(user_info)
        if status != ErrorCode.Success:
            return status, data
        else:
            return status, data["unionid"]

    @classmethod
    async def add_user_by_range_id(cls, user_info):
        """
        随机生成unionid并新增用户
        :param user_info: 用户信息
        """
        # 随机生成一个6位的id，并确保没有重复
        while True:
            random_int = random.randint(10000, 99999)
            # 查询是否有重复的, 如果重复的话重新生成一个
            if User.query_user_by_unionid(random_int) is not None:
                continue
            else:
                user_info["unionid"] = random_int
        return cls._add_user(user_info)

    @classmethod
    async def add_user_by_code(cls, user_info):
        """
        通过unionid新增用户
        :param user_info:
        :return:
        """
        # 这时候前端会传入code，以此获取openid(如果测试标识存在，则生成随机的unionid
        if Config.SystemTest == "true":
            user_info["unionid"] = str(uuid4())
        else:
            status, user_data = get_user_info_by_code(user_info["code"])
            if status != ErrorCode.Success:
                return status, None
            # 暂时使用openid，充当unionid
            user_info["unionid"] = user_data["openid"]
        return cls._add_user(user_info)

    @classmethod
    async def update_user(cls, user_info):
        """
        更新用户
        :param user_info:
        :return:
        """
        # 检验数据是否缺失
        if not User.user_info_checker(user_info):
            return ErrorCode.UserInfoError
        # 检验用户是否存在
        user_data = User.query_user_by_id(user_info["id"])
        if user_data is None:
            return ErrorCode.UserNotExists
        # 更新用户
        if not User.update_user(user_info, user_data):
            return ErrorCode.UserUpdateError
        return ErrorCode.Success

    @classmethod
    async def delete_user(cls, user_id):
        """
        删除用户
        :param user_id:
        :return:
        """
        # 检验用户是否存在
        user_data = User.query_user_by_id(user_id)
        if not user_data:
            return ErrorCode.UserNotExists
        # 删除用户
        if not User.delete_user(user_id, user_data):
            return ErrorCode.UserDeleteError
        return ErrorCode.Success

    @staticmethod
    async def update_user_info(user_detail: dict):
        # 转换医生的id为名称
        doctor_data = User.query_user_by_id(user_detail["doctor_id"])
        user_detail["doctor_name"] = doctor_data.user_name if doctor_data else ""
        # 转换医院的id为名称
        hospital_data = Hospital.query_hospital_by_id(user_detail["hospital_id"])
        user_detail["hospital_name"] = hospital_data.name if hospital_data else ""
        return user_detail

    @classmethod
    async def get_user(cls, user_id):
        """
        通过ID查询用户信息
        :param user_id:
        :return:
        """
        user_data = User.query_user_by_id(user_id)
        if not user_data:
            return ErrorCode.UserNotExists
        user_detail = user_data.to_dict()
        user_detail = await cls.update_user_info(user_detail)
        return user_detail

    @classmethod
    async def get_user_info_by_doctor_id(cls, doctor_id):
        """
        通过医生ID查询用户信息
        :param doctor_id:
        :return:
        """
        user_data = User.query_user_by_doctor_id(doctor_id)
        if not user_data:
            return []
        users = []
        for user in user_data:
            # 转换医院的id为名称
            hospital_data = Hospital.query_hospital_by_id(user.hospital_id)
            users.append({
                "name": user.user_name, "id": user.id,
                "hospital_name": hospital_data.name if hospital_data else ""
            })
        return users

    @classmethod
    async def get_user_info_by_hospital_id(cls, hospital_id):
        """
        通过医院ID查询医生
        """
        if not hospital_id:
            hospital_id, _ = Hospital.query_huaqiao_hospital()
        all_user_info = []
        user_data = User.query_user_by_hospital_id(hospital_id, user_type=UserType.DOCTOR)
        for user in user_data:
            user_info = await cls.update_user_info(user.to_dict())
            all_user_info.append(user_info)
        return all_user_info
