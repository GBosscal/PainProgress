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


class LoginView(HTTPMethodView):
    @openapi.summary("登陆")
    @openapi.description("登陆")
    @openapi.parameter("code", location="query")
    @openapi.tag("login")
    async def get(self, request):
        code = request.args.get("code")
        service_code, user_id = LoginService.login(code)
        return response(service_code, {"id": user_id})


login_blueprint = Blueprint("login", "/login", version=1)
login_blueprint.add_route(LoginView.as_view(), "")
