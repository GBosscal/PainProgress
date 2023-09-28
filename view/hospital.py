"""
@Project: BackendForPain
@File: hospital.py
@Auth: Bosscal
@Date: 2023/9/12
@Description:
    医院相关的接口
"""
from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.hospital import HospitalService
from const import ErrorCode


class HospitalData:
    name: str


class UpdateHospital:
    name: str
    id: int


class DeleteHospital:
    id: int


class HospitalView(HTTPMethodView):

    @openapi.summary("获取医院的列表")
    @openapi.description("获取全部医院的名称以及对应的ID")
    @openapi.tag("医院信息管理")
    async def get(self, request):
        data = await HospitalService.get_hospitals()
        return response(ErrorCode.Success, data)

    @openapi.summary("创建一个医院")
    @openapi.description("通过名称创建一个医院")
    @openapi.definition(
        body={"application/json": HospitalData}
    )
    @openapi.definition(body={"name": "医院名称"})
    @openapi.tag("医院信息管理")
    async def post(self, request):
        name = request.json.get("name")
        service_code = await HospitalService.add_hospital(name)
        return response(service_code)

    @openapi.summary("更新一个医院")
    @openapi.description("通过名称更新一个医院")
    @openapi.definition(
        body={"application/json": UpdateHospital}
    )
    @openapi.tag("医院信息管理")
    async def put(self, request):
        name = request.json.get("name")
        hospital_id = request.json.get("id")
        service_code = await HospitalService.update_hospital(hospital_id, name)
        return response(service_code)

    @openapi.summary("删除一个医院")
    @openapi.description("通过ID删除一个医院")
    @openapi.definition(
        body={"application/json": DeleteHospital}
    )
    @openapi.tag("医院信息管理")
    async def delete(self, request):
        hospital_id = request.json.get("id")
        service_code = await HospitalService.delete_hospital(hospital_id)
        return response(service_code)


hospital_blueprint = Blueprint("hospital", "/hospital", version=1)
hospital_blueprint.add_route(HospitalView.as_view(), "")
