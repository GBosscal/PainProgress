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


class CreatePainData:
    patient_id: str
    pain_level_custom: int
    pain_data_path: str


class UpdatePainData:
    pain_id: str
    pain_level_custom: int
    pain_data_path: str


class DeletePainData:
    pain_id: str


class PainDataView(HTTPMethodView):

    @openapi.summary("获取疼痛数据")
    @openapi.description("通过患者的ID获取疼痛数据")
    @openapi.parameter("patient_id", location="query")
    @openapi.tag("疼痛数据管理")
    async def get(self, request):
        patient_id = request.args.get("patient_id")
        data = await PainService.get_pain_data_by_patient_id(patient_id)
        return response(ErrorCode.Success, data)

    @openapi.summary("创建疼痛数据")
    @openapi.description("创建疼痛数据")
    @openapi.definition(
        body={"application/json": CreatePainData}
    )
    @openapi.tag("疼痛数据管理")
    async def post(self, request):
        patient_id = request.json.get("patient_id")
        pain_level_custom = request.json.get("pain_level_custom")
        pain_data_path = request.json.get("pain_data_path")
        service_code, convert_image = await PainService.add_pain_data(
            patient_id, pain_level_custom, pain_data_path)
        return response(service_code, {"convert_image": convert_image})

    @openapi.summary("更新疼痛数据")
    @openapi.description("更新疼痛数据")
    @openapi.definition(
        body={"application/json": UpdatePainData}
    )
    @openapi.tag("疼痛数据管理")
    async def put(self, request):
        pain_id = request.json.get("pain_id")
        pain_level_custom = request.json.get("pain_level_custom")
        pain_data_path = request.json.get("pain_data_path")
        service_code, convert_image = await PainService.update_pain_data(
            pain_id, pain_level_custom, pain_data_path)
        return response(service_code, {"convert_image": convert_image})

    @openapi.summary("删除疼痛数据")
    @openapi.description("删除疼痛数据")
    @openapi.definition(
        body={"application/json": DeletePainData}
    )
    @openapi.tag("疼痛数据管理")
    async def delete(self, request):
        pain_id = request.json.get("pain_id")
        service_code = await PainService.delete_pain_data(pain_id)
        return response(service_code)


pain_blueprint = Blueprint("pain", "/pain", version=1)
pain_blueprint.add_route(PainDataView.as_view(), "")


class ImagePainData:
    pain_data: str
    patient_id: int
    pain_level_custom: int


class PainDataWithUploadDownloadView(HTTPMethodView):
    """
    这个视图将图片的上传下载均集成到里面了。
    """

    @openapi.summary("获取疼痛数据")
    @openapi.description("获取疼痛数据")
    @openapi.parameter("patient_id", location="query")
    @openapi.tag("疼痛数据管理-集成图像处理")
    async def get(self, request):
        patient_id = request.args.get("patient_id")
        data = await PainService.get_pain_data_with_image_by_patient_id(patient_id)
        return response(ErrorCode.Success, data)

    @openapi.summary("获取疼痛数据")
    @openapi.description("获取疼痛数据")
    @openapi.definition(
        body={"application/form-data": ImagePainData}
    )
    @openapi.tag("疼痛数据管理-集成图像处理")
    async def post(self, request):
        # 获取图片数据
        file_data = request.files.get("pain_data")
        # 获取疼痛数据
        patient_id = request.form.get("patient_id")
        pain_level_custom = request.form.get("pain_level_custom")
        service_code, convert_image = await PainService.add_pain_data_with_image(
            patient_id, pain_level_custom, file_data)
        return response(service_code, {"convert_image": convert_image})

    @openapi.summary("获取疼痛数据")
    @openapi.description("获取疼痛数据")
    @openapi.definition(
        body={"application/form-data": ImagePainData}
    )
    @openapi.tag("疼痛数据管理-集成图像处理")
    async def put(self, request):
        # 获取图片数据
        file_data = request.files.get("pain_data")
        # 获取疼痛数据
        pain_id = request.json.get("pain_id")
        pain_level_custom = request.json.get("pain_level_custom")
        service_code, convert_image = await PainService.update_pain_data_with_image(
            pain_id, pain_level_custom, file_data)
        return response(service_code, {"convert_image": convert_image})

    @openapi.summary("删除疼痛数据")
    @openapi.description("删除疼痛数据")
    @openapi.definition(
        body={"application/json": DeletePainData}
    )
    @openapi.tag("疼痛数据管理-集成图像处理")
    async def delete(self, request):
        pain_id = request.json.get("pain_id")
        service_code = await PainService.delete_pain_data(pain_id)
        return response(service_code)


class PainDataStatistics(HTTPMethodView):

    @openapi.summary("获取全部的疼痛数据")
    @openapi.description("获取特定患者全部的疼痛数据")
    @openapi.parameter("patient_id", location="query")
    @openapi.tag("疼痛数据统计")
    async def get(self, request):
        patient_id = request.args.get("patient_id")
        if not patient_id:
            return response(ErrorCode.ParamsMission)
        return_data = await PainService.get_pain_data_statistic_by_patient_id(patient_id)
        return response(ErrorCode.Success, return_data)


pain_with_image_blueprint = Blueprint("pain_data", "/pain/image", version=1)
# 上传文件和创建数据分开
pain_with_image_blueprint.add_route(PainDataView.as_view(), "")
# 上传文件和创建数据合并
pain_with_image_blueprint.add_route(PainDataWithUploadDownloadView.as_view(), "/with_upload")
# 统计患者的疼痛数据，按照创建时间，正序返回
pain_with_image_blueprint.add_route(PainDataStatistics.as_view(), "/statistics")
