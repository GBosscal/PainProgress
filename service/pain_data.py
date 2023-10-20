"""
@Project: BackendForPain
@File: pain_data.py
@Auth: Bosscal
@Date: 2023/9/15
@Description: 
"""
import base64

from model.pain_data import Pain
from const import ErrorCode
from pain_model.convert import convert_img
from utils.storage import build_storage_path
from utils.storage import storage_data
from utils.storage import get_base64_for_image
from utils.storage import build_travel_storage_path


class PainService:

    @classmethod
    async def get_pain_data_by_pain_id(cls, pain_id):
        """
        通过疼痛数据ID获取疼痛数据
        :param pain_id: 疼痛ID
        :return:
        """
        pain_data = Pain.query_pain_data_by_id(pain_id)
        return pain_data.to_dict()

    @classmethod
    async def get_pain_data_by_patient_id(cls, patient_id):
        """
        获取患者的疼痛数据
        :param patient_id: 患者ID
        :return:
        """
        data_list = Pain.query_pain_data_by_patient_id(patient_id)
        return [data.to_dict() for data in data_list]

    @classmethod
    async def get_pain_data_with_image_by_patient_id(cls, patient_id):
        """
        获取患者的疼痛数据以及对应的图片
        :param patient_id: 患者ID
        :return:
        """
        data_list = await cls.get_pain_data_by_patient_id(patient_id)
        for index, data in enumerate(data_list):
            absolute_path, convert_image_path = build_travel_storage_path(data['patient_id'], data["pain_data_path"])
            data["convert_image_path"] = get_base64_for_image(convert_image_path)
            data["image_data"] = get_base64_for_image(absolute_path)
            data_list[index] = data
        return data_list

    @classmethod
    async def add_pain_data(cls, patient_id, pain_level_custom, pain_data_path):
        """
        增加一条患者的疼痛数据
        :param patient_id: 患者ID
        :param pain_level_custom: 患者自定义的疼痛级别
        :param pain_data_path: 疼痛数据的路经
        :return:
        """
        # 先跑一下模型，同步完成数据标注
        absolute_path, convert_image_path = build_travel_storage_path(patient_id, pain_data_path)
        pain_level = convert_img(absolute_path, convert_image_path)
        if not Pain.add_pain_data(
                patient_id=patient_id, pain_level_custom=pain_level_custom,
                pain_data=pain_data_path, pain_level=pain_level
        ):
            return ErrorCode.PainAddError, None
        # 返回画了框的图像的base64数据
        convert_image = get_base64_for_image(convert_image_path)
        return ErrorCode.Success, convert_image

    @classmethod
    async def add_pain_data_with_image(cls, patient_id, pain_level_custom, pain_data):
        """
        增加一条患者的疼痛数据（包括图片）
        :param patient_id: 患者ID
        :param pain_level_custom: 患者自定义的疼痛等级
        :param pain_data: 疼痛影像的数据（流数据）
        :return:
        """
        # 先把流数据落盘
        storage_path = build_storage_path(patient_id, pain_data.name)
        if not storage_data(pain_data, storage_path):
            return ErrorCode.UploadDataError, None
        # 创建一条患者的疼痛数据
        return await cls.add_pain_data(patient_id, pain_level_custom, storage_path)

    @classmethod
    async def update_pain_data(cls, pain_id, pain_level_custom, pain_data_path):
        """
        更新一条患者的疼痛数据
        :param pain_id: 疼痛数据的ID
        :param pain_level_custom: 患者自定义的疼痛等级
        :param pain_data_path: 疼痛数据的路经
        :return:
        """
        # 查询患者的数据是否存在
        pain_data = Pain.query_pain_data_by_id(pain_id)
        if not pain_data:
            return ErrorCode.PainDataNotExists
        # 更新模型标注数据
        _, convert_image_path = build_travel_storage_path(pain_data.patient_id, pain_data_path)
        pain_level = convert_img(pain_data_path, convert_image_path)
        # 更新患者疼痛的数据
        if not Pain.update_pain_data(pain_level_custom, pain_data_path, pain_data, pain_level):
            return ErrorCode.PainUpdateError, None
        # 返回画了框的图像的base64数据
        convert_image = get_base64_for_image(convert_image_path)
        return ErrorCode.Success, convert_image

    @classmethod
    async def update_pain_data_with_image(cls, pain_id, pain_level_custom, pain_data):
        """
        更新一条患者的疼痛数据（包括图片）
        :param pain_id: 疼痛数据的ID
        :param pain_level_custom: 患者自定义的疼痛等级
        :param pain_data: 疼痛的图片
        :return:
        """
        # 先校验患者是否存在
        pain_info = Pain.query_pain_data_by_id(pain_id)
        if not pain_info:
            return ErrorCode.PainDataNotExists
        # 数据落盘
        absolute_path, convert_image_path = build_travel_storage_path(pain_info.patient_id, pain_data.name)
        if not storage_data(pain_data, absolute_path):
            return ErrorCode.UploadDataError
        # 更新模型标注数据
        pain_level = convert_img(absolute_path, convert_image_path)
        # 更新患者疼痛的数据
        if not Pain.update_pain_data(pain_level_custom, absolute_path, pain_info, pain_level):
            return ErrorCode.PainUpdateError, None
        return ErrorCode.Success, convert_image_path

    @classmethod
    async def delete_pain_data(cls, pain_id):
        """
        删除一条疼痛数据
        :param pain_id:
        :return:
        """
        # 查询患者的数据是否存在
        pain_data = Pain.query_pain_data_by_id(pain_id)
        if not pain_data:
            return ErrorCode.PainDataNotExists
        # 删除疼痛的数据
        if not Pain.delete_pain_data(pain_data):
            return ErrorCode.PainDeleteError
        return ErrorCode.Success

    @classmethod
    async def get_pain_data_statistic_by_patient_id(cls, patient_id):
        """
        根据患者ID获取全部的疼痛数据
        """
        return_result = []
        all_pain_data = Pain.query_pain_data_by_patient_id(patient_id)
        for pain_data in all_pain_data:
            pain_data = pain_data.to_dict()
            # 暂时不返回图像内容
            # absolute_path, convert_image_path = build_travel_storage_path(patient_id, pain_data["pain_data"])
            # pain_data.update({
            #     "convert_image": get_base64_for_image(convert_image_path),
            #     "image": get_base64_for_image(absolute_path)
            # })
            return_result.append(pain_data)
        return return_result
