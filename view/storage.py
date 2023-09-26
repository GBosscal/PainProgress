"""
@Project: BackendForPain
@File: storage.py
@Auth: Bosscal
@Date: 2023/9/15
@Description: 
"""

from sanic.views import HTTPMethodView
from sanic.views import stream
from sanic_ext import openapi
from sanic import Blueprint
from sanic.response import file

from view import response
from service.pain_data import PainService
from const import ErrorCode
from utils.storage import build_storage_path
from utils.storage import storage_data


class StorageView(HTTPMethodView):

    @openapi.summary("新增一条疼痛数据")
    @openapi.description("新增一条疼痛数据")
    @openapi.body({"pain_data": "疼痛数据", "patient_id": "患者ID"})
    @openapi.tag("数据存储")
    async def post(self, request):
        file_data = request.files.get("pain_data")
        patient_id = request.form.get("patient_id")
        storage_path = build_storage_path(patient_id, file_data.name)
        if not storage_data(file_data.body, storage_path):
            return response(ErrorCode.UploadDataError)
        return response(ErrorCode.Success, data={"path": file_data.name})

    @openapi.summary("获取一条疼痛数据")
    @openapi.description("获取一条疼痛数据")
    @openapi.body({"pain_id": "疼痛数据ID"})
    @openapi.tag("数据存储")
    async def get(self, request):
        pain_id = request.args.get("pain_id")
        pain_data = await PainService.get_pain_data_by_pain_id(pain_id)
        if not pain_data:
            return response(ErrorCode.PainDataNotExists)
        file_name = pain_data['pain_data_path']
        # 数据库只存储了文件名称，所以要再次拼接
        data_path = build_storage_path(pain_data['patient_id'], file_name)
        # 目前强制指定一个jpeg
        return await file(data_path, mime_type="image/jpeg", filename=file_name)


storage_blueprint = Blueprint("storage", "/storage", version=1)
storage_blueprint.add_route(StorageView.as_view(), "")
