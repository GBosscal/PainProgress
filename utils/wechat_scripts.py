"""
@Project: BackendForPain
@File: wechat_scripts.py
@Auth: Bosscal
@Date: 2023/10/7
@Description: 
"""
import requests

from const import AppID, AppSecret, ErrorCode, RedisKey
from utils.redis_helper import set_redis_data, get_redis_data_by_key


def get_access_token():
    # 尝试从redis中获取token，如果没有说明token过期了。
    token = get_redis_data_by_key(RedisKey.AccessTokenKey)
    if token:
        return token
    url = "https://api.weixin.qq.com/cgi-bin/token"
    data = {"grant_type": "client_credential", "appid": AppID, "secret": AppSecret}
    response = requests.get(url=url, params=data)
    if response.status_code != 200:
        return ErrorCode.GetAccessTokenError
    data = response.json()
    if data["errcode"] != 0:
        return ErrorCode.GetAccessTokenError
    # 更新数据到redis中
    set_redis_data(RedisKey.AccessTokenKey, data["access_token"], data["expires_in"])
    return data["access_token"]


def get_user_info_by_code(code):
    url = "https://api.weixin.qq.com/sns/jscode2session"
    data = {"appid": AppID, "secret": AppSecret, "js_code": code, "grant_type": "authorization_code"}
    response = requests.get(url=url, params=data)
    if response.status_code != 200:
        return ErrorCode.GetAccessTokenError, None
    data = response.json()
    error_code = data.get("errcode")
    if error_code and error_code != 0:
        return ErrorCode.GetAccessTokenError, None
    return ErrorCode.Success, data
