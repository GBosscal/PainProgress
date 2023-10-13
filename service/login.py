"""
@Project: BackendForPain
@File: login.py
@Auth: Bosscal
@Date: 2023/10/12
@Description: 
"""
from utils.wechat_scripts import get_user_info_by_code
from model.user import User
from const import ErrorCode


class LoginService:

    @classmethod
    async def login(cls, code):
        # 请求微信官方，
        status, user_data = get_user_info_by_code(code)
        if status:
            return status, None
        # 暂时先用openID
        user_code = user_data.get("openid")
        # 查询用户是否已经注册
        user_info = User.query_user_by_unionid(user_code)
        if not user_info:
            return ErrorCode.UserNotRegistry, None
        else:
            return ErrorCode.Success, user_info.id
