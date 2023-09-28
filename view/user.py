from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.user import UserService
from const import ErrorCode, ErrorMsg


class CreateUser:
    user_name: str
    hospital_id: int
    user_type: str
    wechat_id: str
    doctor_id: int
    age: int


class UpdateUser:
    user_name: str
    hospital_id: int
    user_type: str
    doctor_id: int
    age: int
    id: int


class DeleteUser:
    user_id: int


class UserView(HTTPMethodView):

    @openapi.summary("获取用户的信息")
    @openapi.description("获取用户的信息")
    @openapi.parameter("user_id", location="query")
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
        body={"application/json": CreateUser}
    )
    @openapi.tag("user")
    async def post(self, request):
        request_body = request.json
        service_code = await UserService.add_user(request_body)
        return response(service_code)

    @openapi.summary("更新用户")
    @openapi.description("更新用户")
    @openapi.definition(
        body={"application/json": UpdateUser}
    )
    @openapi.tag("user")
    async def put(self, request):
        request_body = request.json
        service_code = await UserService.update_user(request_body)
        return response(service_code)

    @openapi.summary("删除用户")
    @openapi.description("删除用户")
    @openapi.definition(
        body={"application/json": DeleteUser}
    )
    @openapi.tag("user")
    async def delete(self, request):
        user_id = request.json.get("user_id")
        if not user_id:
            return response(ErrorCode.UserIDMissing)
        service_code = await UserService.delete_user(user_id)
        if service_code != ErrorCode.Success:
            return response(service_code)
        return response(ErrorCode.Success)


user_blueprint = Blueprint("user", "/user", version=1)
user_blueprint.add_route(UserView.as_view(), "")
