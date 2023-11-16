from sanic.views import HTTPMethodView
from sanic_ext import openapi
from sanic import Blueprint
from view import response

from service.user import UserService
from const import ErrorCode, ErrorMsg


class CreateUser:
    user_name: str
    hospital_id: str
    user_type: str
    code: str
    doctor_id: str
    age: int


class UpdateUser:
    user_name: str
    hospital_id: str
    user_type: str
    doctor_id: str
    age: int
    id: str


class DeleteUser:
    user_id: str


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
        service_code, user_info = await UserService.add_user_by_code(request_body)
        return response(service_code, user_info)

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


class PatientView(HTTPMethodView):

    @openapi.summary("获取特定医生下的患者")
    @openapi.description("通过医生的ID获取该医生下所有患者的ID以及名称")
    @openapi.tag("user")
    @openapi.parameter("doctor_id", location="query")
    async def get(self, request):
        doctor_id = request.args.get("doctor_id")
        if not doctor_id:
            return response(ErrorCode.UserIDMissing)
        result = await UserService.get_user_info_by_doctor_id(doctor_id)
        return response(ErrorCode.Success, result)


class DoctorView(HTTPMethodView):

    @openapi.summary("获取特定医院下的医生")
    @openapi.description("获取特定医院下的医生")
    @openapi.tag("user")
    @openapi.parameter("hospital_id", location="query")
    async def get(self, request):
        hospital_id = request.args.get("hospital_id")
        if not hospital_id:
            return response(ErrorCode.HospitalIDMissing)
        result = await UserService.get_user_info_by_hospital_id(hospital_id)
        return response(ErrorCode.Success, result)


user_blueprint = Blueprint("user", "/user", version=1)
user_blueprint.add_route(UserView.as_view(), "")
user_blueprint.add_route(PatientView.as_view(), uri="/patient")
user_blueprint.add_route(DoctorView.as_view(), uri="/doctor")

# patient_blueprint = Blueprint("patient", "/user", version=1)
# patient_blueprint.add_route(PatientView.as_view(), uri="/patient")
#
# doctor_blueprint =  Blueprint("doctor", "/doctor", version=1)
# doctor_blueprint.add_route(DoctorView.as_view(), uri="")
