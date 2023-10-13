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


class LoginService:

    @classmethod
    async def login(cls, code):
        # 请求微信官方，
        status, user_data = get_user_info_by_code(code)
        if status != ErrorCode.Success:
            return status, None
        # 暂时先用openID
        user_code = user_data.get("openid")
        # 查询用户是否已经注册
        user_info = User.query_user_by_unionid(user_code)
        if not user_info:
            return ErrorCode.UserNotRegistry, None
        else:
            # 直接将用户信息返回给前端
            user_info = user_info.to_dict()
            user_info = await UserService.update_user_info(user_info)
            return ErrorCode.Success, user_info

