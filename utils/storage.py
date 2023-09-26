"""
@Project: BackendForPain
@File: storage.py
@Auth: Bosscal
@Date: 2023/9/12
@Description:
"""
import os
import base64

from const import PainDataPath


def build_storage_path(patient_id, file_name):
    """
    构建疼痛数据存储的路经
    :param patient_id:患者ID
    :param file_name:文件名称
    :return:
    """
    dir_path = os.path.join(PainDataPath, f"patient_{patient_id}")
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, file_name)
    return file_path


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
            encoded_string = base64.b64encode(f.read())
    except Exception:
        return ""
    return encoded_string
