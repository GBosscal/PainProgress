"""
@Project: BackendForPain
@File: log.py
@Auth: Bosscal
@Date: 2023/9/11
@Description:
    定义日志的样式，格式，存储日志的路经等。
"""
import os
from loguru import logger

from const import LogPath


class CustomLogging:

    def __init__(self, dir_path=LogPath, file_name="app.log"):
        os.makedirs(dir_path, exist_ok=True)
        self.file_name = file_name
        self.my_logger = logger
        self.my_logger.add(file_name, encoding='utf-8', retention="7d")

    def info(self, content):
        self.my_logger.info(content)

    def debug(self, content):
        self.my_logger.debug(content)

    def error(self, content):
        self.my_logger.error(content)

    def critical(self, content):
        self.my_logger.critical(content)

    def warning(self, content):
        self.my_logger.warning(content)

    def success(self, content):
        self.my_logger.success(content)

    def trace(self, content):
        self.my_logger.trace(content)

    def traceback(self):
        import traceback
        self.my_logger.error(f'执行失败！！！失败信息：\n {traceback.format_exc()}')

# # 自定义日志句柄
# custom_logger = CustomLogging(os.path.join(LogPath, "app.log"))


# def wrapper_log(func):
#     """
#     无参装饰器，也可以写成有参装饰器，True或Flase标记是否调用日志模块
#     功能一：执行失败，打印并记录错误日志信息，定位bug
#     功能二：记录用例执行时间
#     :param func:
#     :return:
#     """
#
#     func_logger = CustomLogging(os.path.join(LogPath, "func.log"))
#
#     @wraps(func)  # wraps使inner装的更像一个func
#     def inner(*args, **kwargs):
#         func_logger.info(f'{func.__name__}---->函数开始执行')
#         start = time.time()
#         try:
#             func(*args, **kwargs)
#         except Exception as e:
#             func_logger.error(f'{func.__name__}函数执行失败，失败原因：{e}')
#             raise e
#         end = time.time()
#         func_logger.info(f'{func.__name__}用例执行成功！！！，用例执行用时:{int(end - start)}ms')
#         return func
#
#     return inner
