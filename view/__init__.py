from sanic.response import json
from const import ErrorCode, ErrorMsg


# def success_response(data, code=0, msg=""):
#     """
#     正常返回的统一方法
#     :param code: 返回代码（暂定0等于正常，其他表示异常）
#     :param data: 返回的数据
#     :param msg: 返回的信息
#     :return:
#     """
#     if data is None:
#         data = {}
#     return json({"code": code, "data": data, "msg": msg})
#
#
# def error_response(data, code=3, msg=""):
#     """
#     异常返回的统一方法
#     :param code: 返回代码（暂定0等于正常，其他表示异常）
#     :param data: 返回的数据
#     :param msg: 返回的信息
#     :return:
#     """
#     if data is None:
#         data = {}
#     return json({"code": code, "data": data, "msg": msg})


def response(service_code, data=None):
    """
    返回封装的统一方法
    :param data: 响应的数据
    :param service_code: 服务端返回的代码
    :return:
    """
    if data is None:
        data = {}
    return json({"code": service_code.value, "msg": ErrorMsg[service_code.name].value, "data": data})
