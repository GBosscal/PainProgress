"""
@Project: BackendForPain
@File: feedback.py
@Auth: Bosscal
@Date: 2023/9/15
@Description: 
"""

from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.feedback import FeedbackService
from const import ErrorCode


class CreateMsg:
    receiver: str
    sender: str
    msg: str


class DeleteMsg:
    msg_id: str


class FeedbackView(HTTPMethodView):

    @openapi.summary("获取反馈信息")
    @openapi.description("通过receiver，sender获取指定用户之间的信息")
    @openapi.parameter("receiver", location="query")
    @openapi.parameter("sender", location="query")
    @openapi.tag("反馈管理")
    async def get(self, request):
        receiver = request.args.get("receiver")
        sender = request.args.get("sender")
        return response(ErrorCode.Success, FeedbackService.get_msg_by_user_id(receiver, sender))

    @openapi.summary("创建一条反馈信息")
    @openapi.description("创建一条反馈信息")
    @openapi.definition(
        body={"application/json": CreateMsg}
    )
    @openapi.tag("反馈管理")
    async def post(self, request):
        receiver = request.json.get("receiver")
        sender = request.json.get("sender")
        msg = request.json.get("msg")
        service_code = FeedbackService.add_msg(receiver, sender, msg)
        return response(service_code)

    @openapi.summary("删除一条反馈信息")
    @openapi.description("删除一条反馈信息")
    @openapi.definition(
        body={"application/json": DeleteMsg}
    )
    @openapi.tag("反馈管理")
    async def delete(self, request):
        msg_id = request.json.get("msg_id")
        service_code = FeedbackService.delete_msg(msg_id)
        return response(service_code)


feedback_blueprint = Blueprint("feedback", url_prefix="/feedback", version=1)
feedback_blueprint.add_route(FeedbackView.as_view(), uri="")
