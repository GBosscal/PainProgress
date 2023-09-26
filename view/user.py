from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.user import UserService
from const import ErrorCode, ErrorMsg


class UserView(HTTPMethodView):

    @openapi.summary("获取用户的信息")
    @openapi.description("获取用户的信息")
    @openapi.definition(body={"user_id": "用户ID"})
    @openapi.tag("user")
    async def get(self, request):
        user_id = request.args.get("user_id")
        user_data = await UserService.get_user(user_id)
        if isinstance(user_data, ErrorCode):
            return response(user_data)
        return response(ErrorCode.Success, user_data)

    @openapi.summary("创建用户")
    @openapi.description("创建用户")
    @openapi.definition(
        body={
            "user_name": "用户名称", "hospital_id": "医院ID", "user_type": "用户类型（doctor,patient)",
            "wechat_id": "微信ID", "doctor_id": "医生ID", "age": "年龄"
        }
    )
    @openapi.tag("user")
    async def post(self, request):
        request_body = request.json
        service_code = await UserService.add_user(request_body)
        return response(service_code)

    @openapi.summary("更新用户")
    @openapi.description("更新用户")
    @openapi.definition(
        body={
            "user_name": "用户名称", "hospital_id": "医院ID", "user_type": "用户类型（doctor,patient)",
            "doctor_id": "医生ID", "age": "年龄", "id": "用户ID"
        }
    )
    @openapi.tag("user")
    async def put(self, request):
        request_body = request.json
        service_code = await UserService.update_user(request_body)
        return response(service_code)

    @openapi.summary("删除用户")
    @openapi.description("删除用户")
    @openapi.definition(body={"user_id": "用户ID"})
    @openapi.tag("user")
    async def delete(self, request):
        user_id = request.json.get("user_id")
        if not user_id:
            return response(ErrorCode.UserIDMissing)
        service_code = await UserService.delete_user(user_id)
        if service_code != ErrorCode.Success:
            return response(service_code)


user_blueprint = Blueprint("user", "/user", version=1)
user_blueprint.add_route(UserView.as_view(), "")
