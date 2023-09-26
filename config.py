"""
@Project: BackendForPain
@File: config.py
@Auth: Bosscal
@Date: 2023/9/4
@Description:
    系统配置的具体描述。
    实现方案：
        分模块定义初始值，并根据需要通过环境变量进行覆盖。
        构建时，仅需要将相应的系统属性放到环境中即可。
"""

import os


class MysqlConfig:
    MysqlHost = os.environ.get("mysql_host", "127.0.0.1")
    MysqlPort = int(os.environ.get("mysql_port", "3306"))
    MysqlUserName = os.environ.get("mysql_name", "admin")
    MysqlPSWD = os.environ.get("mysql_pswd", "admin")
    MysqlDataBase = os.environ.get("mysql_db", "pain")
    MysqlEcho = False if os.environ.get("mysql_echo") != "true" else True


class SystemConfig:
    SysHost = os.environ.get("system_host", "0.0.0.0")
    SysPort = os.environ.get("system_port", 25800)
    SysWorkerNum = os.environ.get("system_worker", 10)


class Config(MysqlConfig, SystemConfig):

    @classmethod
    def get_mysql_url(cls):
        return f"mysql+pymysql://{cls.MysqlUserName}:{cls.MysqlPSWD}@{cls.MysqlHost}:{cls.MysqlPort}/{cls.MysqlDataBase}"
