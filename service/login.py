"""
@Project: BackendForPain
@File: login.py
@Auth: Bosscal
@Date: 2023/10/12
@Description: 
"""
from utils.wechat_scripts import get_user_info_by_code
from service.user import UserService
from model.user import User
from const import ErrorCode
from utils.secret import check_password, hash_string_with_timestamp
from utils.redis_helper import set_redis_data
from model.hospital import Hospital


class LoginService:

    @classmethod
    def _set_token(cls, user_id):
        token = hash_string_with_timestamp(user_id)
        # set_redis_data(f"token:{token}", user_id, 60 * 60)
        return token

    @classmethod
    async def login(cls, code):
        """
        通过微信Code登陆
        """
        # 请求微信官方
        status, user_data = get_user_info_by_code(code)
        if status != ErrorCode.Success:
            return status, None
        # 暂时先用openID
        user_code = user_data.get("openid")
        # 查询用户是否已经注册
        user_info = User.query_user_by_unionid(user_code)
        if not user_info:
            return ErrorCode.UserNotRegistry, None
        # 更新用户登陆使用的open——id
        User.update_user_login_openid(user_info, code)
        # 登陆后要设定使用时长，比如1h
        token = cls._set_token(user_info.id)
        # 直接将用户信息返回给前端
        user_info = user_info.to_dict()
        user_info = await UserService.update_user_info(user_info)
        user_info["token"] = token
        # 再返回一个华侨医院的ID回去
        hp_id, hp_name = Hospital.query_huaqiao_hospital()
        user_info["huaqiao_id"] = hp_id
        user_info["huaqiao_name"] = hp_name
        return ErrorCode.Success, user_info

    @classmethod
    async def login_by_password(cls, unionid, passwd, code):
        """
        通过账号密码登陆
        """
        # 查询用户是否已经注册
        user_info = User.query_user_by_unionid(unionid)
        if not user_info:
            return ErrorCode.UserNotRegistry, None
        # 校验密码是否正确
        if not check_password(passwd, user_info.password):
            return ErrorCode.UserPasswordError, None
        # 登陆后要设定使用时长，比如1h
        token = cls._set_token(user_info.id)
        # 更新用户登陆使用的open——id
        User.update_user_login_openid(user_info, code)
        # 直接将用户信息返回给前端
        user_info = user_info.to_dict()
        user_info = await UserService.update_user_info(user_info)
        user_info["token"] = token
        # 再返回一个华侨医院的ID回去
        hp_id, hp_name = Hospital.query_huaqiao_hospital()
        user_info["huaqiao_id"] = hp_id
        user_info["huaqiao_name"] = hp_name
        return ErrorCode.Success, user_info

    @classmethod
    async def get_user_id_by_code(cls, code):
        """
        通过微信的code，获取登陆过的用户id以及名称
        """
        user_list = User.query_user_by_code(code)
        users = [{"name": user["user_name"], "id": user["unionid"]} for user in user_list]
        return users
