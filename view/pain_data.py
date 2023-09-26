"""
@Project: BackendForPain
@File: pain_data.py
@Auth: Bosscal
@Date: 2023/9/15
@Description: 
"""
from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.pain_data import PainService
from const import ErrorCode


class PainDataView(HTTPMethodView):

    @openapi.summary("获取疼痛数据")
    @openapi.description("通过患者的ID获取疼痛数据")
    @openapi.body({"patient_id": "患者ID"})
    @openapi.tag("疼痛数据管理")
    async def get(self, request):
        patient_id = request.args.get("patient_id")
        data = await PainService.get_pain_data_by_patient_id(patient_id)
        return response(ErrorCode.Success, data)

    @openapi.summary("创建疼痛数据")
    @openapi.description("创建疼痛数据")
    @openapi.body({"patient_id": "患者ID", "pain_level_custom": "患者自定义的疼痛级别","pain_data_path": "疼痛影像路经"})
    @openapi.tag("疼痛数据管理")
    async def post(self, request):
        patient_id = request.json.get("patient_id")
        pain_level_custom = request.json.get("pain_level_custom")
        pain_data_path = request.json.get("pain_data_path")
        service_code = await PainService.add_pain_data(patient_id, pain_level_custom, pain_data_path)
        return response(service_code)

    @openapi.summary("更新疼痛数据")
    @openapi.description("更新疼痛数据")
    @openapi.body({"pain_id": "疼痛数据ID", "pain_level_custom": "患者自定义的疼痛级别", "pain_data_path": "疼痛影像路经"})
    @openapi.tag("疼痛数据管理")
    async def put(self, request):
        pain_id = request.json.get("pain_id")
        pain_level_custom = request.json.get("pain_level_custom")
        pain_data_path = request.json.get("pain_data_path")
        service_code = await PainService.update_pain_data(pain_id, pain_level_custom, pain_data_path)
        return response(service_code)

    @openapi.summary("删除疼痛数据")
    @openapi.description("删除疼痛数据")
    @openapi.body({"pain_id": "疼痛数据ID"})
    @openapi.tag("疼痛数据管理")
    async def delete(self, request):
        pain_id = request.json.get("pain_id")
        service_code = await PainService.delete_pain_data(pain_id)
        return response(service_code)


pain_blueprint = Blueprint("pain", "/pain", version=1)
pain_blueprint.add_route(PainDataView.as_view(), "")


class PainDataWithUploadDownloadView(HTTPMethodView):
    """
    这个视图将图片的上传下载均集成到里面了。
    """

    @openapi.summary("获取疼痛数据")
    @openapi.description("获取疼痛数据")
    @openapi.body({"patient_id": "患者ID"})
    @openapi.tag("疼痛数据管理-集成图像处理")
    async def get(self, request):
        patient_id = request.args.get("patient_id")
        data = await PainService.get_pain_data_with_image_by_patient_id(patient_id)
        return response(ErrorCode.Success, data)

    @openapi.summary("获取疼痛数据")
    @openapi.description("获取疼痛数据")
    @openapi.body({"pain_data": "患者的疼痛图像", "patient_id": "患者疼痛数据", "pain_level_custom": "患者自定义的疼痛等级"})
    @openapi.tag("疼痛数据管理-集成图像处理")
    async def post(self, request):
        # 获取图片数据
        file_data = request.files.get("pain_data")
        # 获取疼痛数据
        patient_id = request.form.get("patient_id")
        pain_level_custom = request.form.get("pain_level_custom")
        service_code = await PainService.add_pain_data_with_image(patient_id, pain_level_custom, file_data)
        return response(service_code)

    @openapi.summary("获取疼痛数据")
    @openapi.description("获取疼痛数据")
    @openapi.body({"pain_data": "患者的疼痛图像", "pain_id": "疼痛数据ID", "pain_level_custom": "患者自定义的疼痛等级"})
    @openapi.tag("疼痛数据管理-集成图像处理")
    async def put(self, request):
        # 获取图片数据
        file_data = request.files.get("pain_data")
        # 获取疼痛数据
        pain_id = request.json.get("pain_id")
        pain_level_custom = request.json.get("pain_level_custom")
        service_code = await PainService.update_pain_data_with_image(pain_id, pain_level_custom, file_data)
        return response(service_code)

    @openapi.summary("删除疼痛数据")
    @openapi.description("删除疼痛数据")
    @openapi.body({ "pain_id": "疼痛数据ID"})
    @openapi.tag("疼痛数据管理-集成图像处理")
    async def delete(self, request):
        pain_id = request.json.get("pain_id")
        service_code = await PainService.delete_pain_data(pain_id)
        return response(service_code)


pain_with_image_blueprint = Blueprint("pain", "/pain/image", version=1)
pain_with_image_blueprint.add_route(PainDataView.as_view(), "")
