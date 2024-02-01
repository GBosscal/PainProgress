from enum import Enum as EnumBase

# 日志路经
LogPath = "logs"

# 疼痛数据存储的路经
PainDataPath = "pain_data"

# Token密钥
AppSecretKey = b'painData12345678'

# APP ID
AppID = "wx9acf3f3f48c20d8d"

# APP Secret
AppSecret = "93e62d1d3535a4abb8ebcd37b0dcc4f0"

# 人脸模型权重
detection_model_path = 'pain_model/weight/haarcascade_frontalface_default.xml'

# 权重
emotion_model_path = 'pain_model/weight/E135_0.6466.pth'

_very = [0, 4]
_not_fount = [1, 3, 5]
_bit = [2, 6]

emotion_labels = {
    **{str(k): "非常疼痛" for k in _very},
    **{str(k): "没有发现疼痛" for k in _not_fount},
    **{str(k): "疼痛" for k in _bit}
}

# 用户id起始数，修改的时候要看数据库数据分布情况，否则用户会重复
PreUserID = 10000

# 重置密码密钥
ResetPasswordSecret = "ResetPainServicePassword!@#$"

# 重置后的密码
AfterResetPassword = "abc123@"


class TestUser(EnumBase):
    """
    测试用户 code -> unionid
    """
    f331bf8eb065 = "35c713b9-287e-43be-ac2f-3b815a758842"  # 医生A
    dde666c09144 = "74aab67e-c175-4b31-b3db-d936a525ec55"  # 患者A
    ab0e85b60969 = "822c957a-f219-487d-85f8-f934fcf94c41"  # 患者B


class UserType(EnumBase):
    """
    用户类型的常量定义
    """
    DOCTOR = "doctor"
    PATIENT = "patient"


class DeleteOrNot(EnumBase):
    """
    用户是否被删除的常量定义
    """
    Deleted = True
    NotDeleted = False


class ErrorCode(EnumBase):
    """
    错误代码的常量定义
    """
    Success = "0"
    ParamsMission = "101"

    # 用户异常
    UserInfoError = "10000100"
    UserAlreadyExists = "10000101"
    UserAddError = "10000102"
    UserNotExists = "10000103"
    UserUpdateError = "10000104"
    UserIDMissing = "10000105"
    UserDeleteError = "10000106"
    UserNotRegistry = "10000107"
    UserPasswordError = "10000108"
    UserResetPasswordError = "10000109"
    UserPasswordResetFailed = "10000110"

    # 医院异常
    HospitalExists = "100000201"
    HospitalAddError = "10000202"
    HospitalNotExists = "10000203"
    HospitalUpdateError = "10000204"
    HospitalDeleteError = "10000205"
    HospitalIDMissing = "10000305"

    # 疼痛数据异常
    PainAddError = "10000301"
    PainUpdateError = "10000302"
    PainDeleteError = "10000303"
    PainDataNotExists = "10000304"

    # 疼痛文件异常
    UploadDataError = "10000401"
    DownloadDataError = "10000402"

    # 反馈相关异常
    AddMsgError = "10000501"
    DeleteMsgError = "10000502"
    MsgNotExists = "10000503"

    # 微信请求异常
    GetAccessTokenError = "10000601"

    # 文件路径异常
    FilePathError = "10000701"
    FileNotExists = "10000702"


class ErrorMsg(EnumBase):
    """
    错误信息的常量定义
    """
    Success = "操作成功"
    ParamsMission = "必要参数缺失"

    # 用户异常
    UserInfoError = "用户信息校验异常"
    UserAlreadyExists = "用户已经存在（相同微信ID）"
    UserAddError = "用户新增异常"
    UserNotExists = "用户不存在"
    UserUpdateError = "用户更新失败"
    UserIDMissing = "用户ID缺失"
    UserDeleteError = "用户删除异常"
    UserNotRegistry = "用户还没注册"
    UserPasswordError = "密码错误"
    UserResetPasswordError = "密码重置条件异常"
    UserPasswordResetFailed = "密码重置失败"

    # 医院异常
    HospitalExists = "医院已经存在"
    HospitalAddError = "医院新增失败"
    HospitalNotExists = "医院不存在"
    HospitalUpdateError = "医院更新异常"
    HospitalDeleteError = "医院删除异常"
    HospitalIDMissing = "医院ID缺失"

    # 疼痛数据异常
    PainAddError = "疼痛数据新增异常"
    PainUpdateError = "疼痛数据更新异常"
    PainDeleteError = "疼痛数据删除异常"
    PainDataNotExists = "疼痛数据不存在"

    # 疼痛文件异常
    UploadDataError = "文件上传异常"
    DownloadDataError = "文件下载异常"

    # 反馈相关异常
    AddMsgError = "新增反馈失败"
    DeleteMsgError = "删除反馈失败"
    MsgNotExists = "反馈不存在"

    # 微信异常
    GetAccessTokenError = "获取微信token异常"

    # 文件异常
    FilePathError = "文件路径异常"
    FileNotExists = "文件不存在"


class RedisKey:
    AccessTokenKey = "wechat_access_token"
