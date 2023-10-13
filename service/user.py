from model.user import User
from model.hospital import Hospital
from const import ErrorCode
from utils.wechat_scripts import get_user_info_by_code


class UserService:

    @classmethod
    async def add_user(cls, user_info):
        """
        新增用户
        :param user_info:
        :return:
        """
        # 这时候前端会传入code，以此获取openid
        status, user_data = get_user_info_by_code(user_info["code"])
        if status:
            return status
        # 暂时使用openid，充当unionid
        user_info["unionid"] = user_data["openid"]
        # 检验数据是否缺失
        if not User.user_info_checker(user_info):
            return ErrorCode.UserInfoError
        # 校验用户（同一个微信ID）是否存在
        if User.query_user_by_unionid(user_info["unionid"]) is not None:
            return ErrorCode.UserAlreadyExists
        # 新增用户
        if not User.add_user(user_info):
            return ErrorCode.UserAddError
        return ErrorCode.Success

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
    async def update_user_info(user_detail:dict):
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
