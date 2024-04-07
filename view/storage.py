"""
@Project: BackendForPain
@File: storage.py
@Auth: Bosscal
@Date: 2023/9/15
@Description: 
"""
import os.path

from sanic.views import HTTPMethodView
from sanic.views import stream
from sanic_ext import openapi
from sanic import Blueprint
from sanic.response import file

from view import response
from service.pain_data import PainService
from const import ErrorCode
from utils import get_mime_type_and_name
from utils.storage import build_storage_path, storage_data


class CreatePainData:
    pain_data: str
    patient_id: str


class StorageView(HTTPMethodView):

    @openapi.summary("新增一条疼痛数据")
    @openapi.description("新增一条疼痛数据")
    @openapi.definition(
        body={"application/json": CreatePainData}
    )
    @openapi.tag("数据存储")
    async def post(self, request):
        file_data = request.files.get("pain_data")
        patient_id = request.form.get("patient_id")
        storage_path = build_storage_path(patient_id, file_data.name)
        if not storage_data(file_data.body, storage_path):
            return response(ErrorCode.UploadDataError)
        return response(ErrorCode.Success, data={"path": file_data.name})

    @openapi.summary("根据疼痛数据id获取对应的图片")
    @openapi.description("根据疼痛数据id获取对应的图片")
    @openapi.parameter("pain_id", location="query")
    @openapi.tag("数据存储")
    async def get(self, request):
        pain_id = request.args.get("pain_id")
        pain_data = await PainService.get_pain_data_by_pain_id(pain_id)
        if not pain_data:
            return response(ErrorCode.PainDataNotExists)
        file_name = pain_data['pain_data']
        # 数据库只存储了文件名称，所以要再次拼接
        data_path = build_storage_path(pain_data['patient_id'], file_name)
        # 目前强制指定一个jpeg
        return await file(data_path, mime_type="image/jpeg", filename=file_name)


class GetStorageView(HTTPMethodView):

    @openapi.summary("根据路径获取数据")
    @openapi.description("根据路径获取数据")
    @openapi.parameter("record_path", location="query")
    @openapi.tag("数据存储")
    async def get(self, request):
        record_path = request.args.get("record_path")
        if not record_path.startswith("pain_data/patient"):
            return response(ErrorCode.FilePathError)
        file_data = await PainService.file_exists(record_path)
        if isinstance(file_data, ErrorCode):
            return response(file_data)
        mime_type, file_name = get_mime_type_and_name(record_path)
        return await file(record_path, mime_type=mime_type, filename=file_name)


storage_blueprint = Blueprint("storage", "/storage", version=1)
storage_blueprint.add_route(StorageView.as_view(), "")
storage_blueprint.add_route(GetStorageView.as_view(), "/get_file")
