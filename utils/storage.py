"""
@Project: BackendForPain
@File: storage.py
@Auth: Bosscal
@Date: 2023/9/12
@Description:
"""
import os
import base64
from uuid import uuid4

from const import PainDataPath


def get_storage_dir(patient_id):
    """
    获取存储的基本路经
    """
    base_dir = os.path.join(PainDataPath, f"patient_{patient_id}")
    return base_dir


def build_storage_path(patient_id, file_name):
    """
    构建疼痛数据存储的路经
    :param patient_id:患者ID
    :param file_name:文件名称
    :return:
    """
    dir_path = get_storage_dir(patient_id)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, file_name)
    return file_path


def build_travel_storage_path(patient_id, file_name=None):
    """
    根据原有的路经，构建一个新的存储路经，用于存储加了标识框的图片。
    """
    if file_name is None:
        file_name = f"{str(uuid4)}.jpg"
    absolute_path = os.path.join(get_storage_dir(patient_id), file_name)
    _tmp = absolute_path.split(".")
    file_front_name, file_back_name = _tmp[0], _tmp[1]
    convert_image_path = file_front_name + "_travel." + file_back_name
    return absolute_path, convert_image_path


def storage_data(file_data, file_path):
    try:
        with open(file_path, "wb") as f:
            f.write(file_data)
    except Exception:
        return False
    return True


def get_base64_for_image(file_path):
    try:
        with open(file_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
    except Exception:
        return ""
    return encoded_string
