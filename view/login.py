"""
@Project: BackendForPain
@File: login.py
@Auth: Bosscal
@Date: 2023/10/7
@Description: 
"""

from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.login import LoginService
from const import ErrorCode


class LoginWithPassword:
    user_id: str
    user_password: str
    code: str


class LoginView(HTTPMethodView):
    @openapi.summary("登陆")
    @openapi.description("登陆")
    @openapi.parameter("code", location="query")
    @openapi.tag("login")
    async def get(self, request):
        code = request.args.get("code")
        if not code:
            return response(ErrorCode.ParamsMission)
        service_code, user_info = await LoginService.login(code)
        return response(service_code, user_info)

    @openapi.summary("登陆-账号密码")
    @openapi.description("登陆-账号密码")
    @openapi.definition(body={"application/json": LoginWithPassword})
    @openapi.tag("login")
    async def post(self, request):
        user_id = request.json.get("user_id")
        user_password = request.json.get("user_password")
        code = request.json.get("code")
        if not user_id or not user_password:
            return response(ErrorCode.ParamsMission)
        service_code, user_info = await LoginService.login_by_password(user_id, user_password, code)
        return response(service_code, user_info)


class SearchUserView(HTTPMethodView):

    @openapi.summary("通过code获取登陆过的用户")
    @openapi.description("通过code获取登陆过的用户")
    @openapi.parameter("code", location="query")
    @openapi.tag("login")
    async def get(self, request):
        code = request.args.get("code")
        if not code:
            return response(ErrorCode.ParamsMission)
        user_data = await LoginService.get_user_id_by_code(code)
        return response(ErrorCode.Success, user_data)


login_blueprint = Blueprint("login", "/login", version=1)
login_blueprint.add_route(LoginView.as_view(), "")
login_blueprint.add_route(SearchUserView.as_view(), "/search_user")
